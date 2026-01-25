const { execSync } = require("child_process");
const core = require("@actions/core");

try {
  const branch = core.getInput("resources-branch");
  const resource = core.getInput("resource-name");
  const target = core.getInput("target-path");

  execSync(`git fetch origin ${branch}`, { stdio: "inherit" });

  try {
    execSync(`git checkout origin/${branch} -- ${resource}`, {
      stdio: "inherit",
    });
    execSync(`mkdir -p ${target} && cp -r ${resource}/. ${target}/`, {
      stdio: "inherit",
    });
  } catch {
    console.log("Resource does not exist yet, skipping fetch");
  }
} catch (err) {
  core.setFailed(err.message);
}
