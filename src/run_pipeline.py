import subprocess
import sys


def run_step(description, command):
    print(f"\n{'=' * 60}")
    print(description)
    print('=' * 60)

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"\nERROR: {description} failed.")
        sys.exit(result.returncode)


def main():
    run_step(
        "STEP 1: Running ETL pipeline",
        ["python", "src/etl.py"]
    )

    run_step(
        "STEP 2: Loading data warehouse",
        ["python", "src/load_warehouse.py"]
    )

    print("\n" + "=" * 60)
    print("FULL PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
