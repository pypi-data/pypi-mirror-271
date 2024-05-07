import subprocess
import sys
from tqdm import tqdm

def upgrade_medicafe(package):
    try:
        # Use tqdm to create a progress bar
        with tqdm(total=100, desc="Upgrading %s" % package, unit="%") as progress_bar:
            # Upgrade the package using pip with --no-cache-dir option
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', package, '--no-cache-dir', '--no-deps', '--disable-pip-version-check'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Update progress bar to 100% upon completion
            progress_bar.update(100 - progress_bar.n)
    except subprocess.CalledProcessError as e:
        # Log the error details
        print("Error: Upgrade failed. Details:", e)
        print("Please check your internet connection and try again later.")
        sys.exit(1)

if __name__ == "__main__":
    medicafe_package = "medicafe"
    upgrade_medicafe(medicafe_package)