const { execSync } = require("child_process");
const core = require("@actions/core");

const MAX_RETRIES = 5;

try {
  const branch = core.getInput("resources-branch");
  const resource = core.getInput("resource-name");
  const target = core.getInput("target-path");
  const token = core.getInput("github-token");

  execSync(`git config user.name "github-actions"`);
  execSync(`git config user.email "github-actions@github.com"`);

  execSync(
    `git remote set-url origin https://x-access-token:${token}@github.com/${process.env.GITHUB_REPOSITORY}.git`
  );

  try {
    execSync(`git checkout ${branch}`, { stdio: "inherit" });
  } catch {
    execSync(`git checkout -b ${branch}`, { stdio: "inherit" });
  }

  execSync(`rm -rf ${resource}`);
  execSync(`mkdir -p ${resource}`);
  execSync(`cp -r ${target}/. ${resource}/`, { stdio: "inherit" });

  execSync(`git add ${resource}`);

  try {
    execSync(`git commit -m "Update ${resource} from CI"`);
  } catch {
    console.log("No changes to commit");
    process.exit(0);
  }

  for (let i = 1; i <= MAX_RETRIES; i++) {
    try {
      execSync(`git pull --rebase origin ${branch}`, { stdio: "inherit" });
      execSync(`git push origin ${branch}`, { stdio: "inherit" });
      process.exit(0);
    } catch {
      console.log(`Retry ${i}/${MAX_RETRIES}`);
    }
  }

  throw new Error("Failed to push resources after retries");
} catch (err) {
  core.setFailed(err.message);
}
