import asyncio
import venv
from pathlib import Path


async def execute_script():
    venv_path = Path("test-script", ".venv")
    venv.create(venv_path)

    # "poetry version;"
    # f"poetry config cache-dir {str(Path(Path().cwd(), 'test-script/sample'))} --local;"
    cmd = (
        "cd test-script;"
        "poetry env use .venv/bin/python3;"
        "poetry config virtualenvs.in-project true --local;"
        "poetry install --no-dev;"
        "poetry run python main.py input/input.json output/output.json"
    )

    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdin, stderr = await process.communicate()

    if stdin:
        print(stdin)

    if process.returncode != 0:
        error_message = f"Command - {cmd} exited with returncode - {process.returncode}"
        if stderr:
            error_message = f"{error_message} - {stderr.decode()}"

        raise OSError(error_message)

    # if not output_filepath.exists():
    #     raise OSError("Output file was not generated")


if __name__ == "__main__":  # pragma: no cover
    print("Hello world")
    asyncio.run(execute_script())
