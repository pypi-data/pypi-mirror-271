import subprocess
import sys
from tqdm import tqdm

def upgrade_medicafe(package):
    try:
        with tqdm(total=100, desc="Upgrading %s" % package, unit="%") as progress_bar:
            # Capture both stdout and stderr
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', package, '--no-cache-dir', '--disable-pip-version-check', '--no-deps'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                # If the return code is non-zero, print error details
                print("Error: Upgrade failed. Details:")
                print("stdout:", result.stdout)
                print("stderr:", result.stderr)
                sys.exit(1)
                
            progress_bar.update(100 - progress_bar.n)
    except Exception as e:
        # Log any other exceptions
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    medicafe_package = "medicafe"
    upgrade_medicafe(medicafe_package)
