import * as NodeFS from "node:fs";

import * as NodeServices from "@effect/platform-node/NodeServices";
import { assert, it } from "@effect/vitest";
import * as Effect from "effect/Effect";
import * as FileSystem from "effect/FileSystem";
import * as Path from "effect/Path";
import { HttpClient, HttpClientResponse } from "effect/http";
import * as ChildProcessSpawner from "effect/process/ChildProcessSpawner";

import * as ProcessRunner from "../processRunner.ts";
import {
  ensurePinnedRuntimeInstalled,
  PinnedRuntimeInstallError,
} from "./pinnedRuntime.ts";

const version = "1.2.3";
const archiveName = `t3-${version}-linux-x64.tar.gz`;

type LabResult = {
  sameOrigin: 0 | 1;
  checksumPass: 0 | 1;
  checksumFail: 0 | 1;
  checksumFailStep: string;
  passUrls: string[];
  failUrls: string[];
  checksumBodyWitness: 0 | 1;
  archiveContainsWitness: 0 | 1;
  tarMocked: 0 | 1;
  extractedBinaryExecuted: 0 | 1;
  loopbackHost: string;
  loopbackPort: number;
  passExtracted: 0 | 1;
  failTarCommands: number;
};

const requiredEnv = (name: string): string => {
  const value = process.env[name];
  if (!value) throw new Error(`missing ${name}`);
  return value;
};

const writeResult = (result: LabResult): void => {
  NodeFS.writeFileSync(requiredEnv("LAB_RESULT_PATH"), `${JSON.stringify(result, null, 2)}\n`);
};

const recordingFetchClient = (requests: string[]) =>
  HttpClient.make((request) =>
    Effect.promise(async () => {
      requests.push(request.url);
      const response = await fetch(request.url);
      const body = await response.arrayBuffer();
      return HttpClientResponse.fromWeb(
        request,
        new Response(body, {
          status: response.status,
          statusText: response.statusText,
          headers: response.headers,
        }),
      );
    }),
  );

const extractingRunner = (
  fs: FileSystem.FileSystem,
  path: Path.Path,
  commands: string[] = [],
) =>
  ProcessRunner.ProcessRunner.of({
    run: (input) =>
      Effect.gen(function* () {
        commands.push(input.command);
        const targetIndex = input.args.indexOf("-C");
        const stagingDir = input.args[targetIndex + 1];
        if (input.command !== "tar" || stagingDir === undefined) {
          return yield* Effect.die(`unexpected command ${input.command}`);
        }
        yield* fs.writeFileString(path.join(stagingDir, "t3"), "#!/bin/sh\n").pipe(Effect.orDie);
        return {
          stdout: "",
          stderr: "",
          code: ChildProcessSpawner.ExitCode(0),
          timedOut: false,
          stdoutTruncated: false,
          stderrTruncated: false,
          stdoutInvalidUtf8: false,
          stderrInvalidUtf8: false,
        };
      }),
  });

const dirnameOf = (url: string): string => url.replace(/\/[^/]*$/, "");

const sameOriginPair = (urls: string[], expectedBase: string): boolean => {
  if (urls.length !== 2) return false;
  const [checksums, archive] = urls;
  if (!checksums.endsWith("/SHA256SUMS")) return false;
  if (!archive.endsWith(`/${archiveName}`)) return false;
  if (dirnameOf(checksums) !== dirnameOf(archive)) return false;
  return checksums.startsWith(`${expectedBase}/`) && archive.startsWith(`${expectedBase}/`);
};

it.layer(NodeServices.layer)("T3-F02-CHECKSUM", (it) => {
  it.effect("same-origin checksum pass then checksum fail against loopback publisher", () =>
    Effect.gen(function* () {
      const fs = yield* FileSystem.FileSystem;
      const path = yield* Path.Path;
      const witness = requiredEnv("LAB_WITNESS");
      const passBase = requiredEnv("LAB_PASS_BASE");
      const failBase = requiredEnv("LAB_FAIL_BASE");
      const loopbackHost = requiredEnv("LAB_LOOPBACK_HOST");
      const loopbackPort = Number(requiredEnv("LAB_LOOPBACK_PORT"));
      const passDir = yield* fs.makeTempDirectoryScoped({ prefix: "t3-f02-pass-" });
      const failDir = yield* fs.makeTempDirectoryScoped({ prefix: "t3-f02-fail-" });
      const passUrls: string[] = [];
      const failUrls: string[] = [];
      const passCommands: string[] = [];
      const failCommands: string[] = [];

      const passPaths = yield* ensurePinnedRuntimeInstalled({
        baseDir: passDir,
        version,
        fs,
        path,
        platform: "linux",
        arch: "x64",
        httpClient: recordingFetchClient(passUrls),
        releaseBaseUrl: passBase,
        runner: extractingRunner(fs, path, passCommands),
        validate: (staging) =>
          fs.exists(staging.entryPath).pipe(
            Effect.flatMap((exists) => (exists ? Effect.void : Effect.die("missing runtime"))),
            Effect.orDie,
          ),
      });

      const failError = yield* ensurePinnedRuntimeInstalled({
        baseDir: failDir,
        version,
        fs,
        path,
        platform: "linux",
        arch: "x64",
        httpClient: recordingFetchClient(failUrls),
        releaseBaseUrl: failBase,
        runner: extractingRunner(fs, path, failCommands),
        validate: () => Effect.die("must not validate an unverified archive"),
      }).pipe(Effect.flip);

      assert.instanceOf(failError, PinnedRuntimeInstallError);

      const checksumBody = NodeFS.readFileSync(
        requiredEnv("LAB_PASS_CHECKSUMS"),
        "utf8",
      );
      const archiveBytes = NodeFS.readFileSync(requiredEnv("LAB_ARCHIVE_PATH"));
      const result: LabResult = {
        sameOrigin:
          sameOriginPair(passUrls, `${passBase}/v${version}`) &&
          sameOriginPair(failUrls, `${failBase}/v${version}`)
            ? 1
            : 0,
        checksumPass:
          passCommands.length === 1 &&
          passCommands[0] === "tar" &&
          (yield* fs.exists(passPaths.sentinelPath))
            ? 1
            : 0,
        checksumFail: failError.step === "verifying the t3 release archive checksum" ? 1 : 0,
        checksumFailStep: failError.step,
        passUrls,
        failUrls,
        checksumBodyWitness: checksumBody.includes(witness) ? 1 : 0,
        archiveContainsWitness: archiveBytes.includes(Buffer.from(witness)) ? 1 : 0,
        tarMocked: 1,
        extractedBinaryExecuted: 0,
        loopbackHost,
        loopbackPort,
        passExtracted: (yield* fs.exists(passPaths.entryPath)) ? 1 : 0,
        failTarCommands: failCommands.length,
      };

      writeResult(result);
      assert.equal(result.sameOrigin, 1);
      assert.equal(result.checksumPass, 1);
      assert.equal(result.checksumFail, 1);
      assert.equal(result.checksumBodyWitness, 1);
      assert.equal(result.archiveContainsWitness, 1);
      assert.equal(result.failTarCommands, 0);
      assert.equal(result.extractedBinaryExecuted, 0);
      assert.equal(yield* fs.readFileString(passPaths.sentinelPath), `${version}\n`);
      assert.deepEqual(yield* fs.readDirectory(path.join(failDir, "runtime", "versions")), []);
    }),
  );
});
