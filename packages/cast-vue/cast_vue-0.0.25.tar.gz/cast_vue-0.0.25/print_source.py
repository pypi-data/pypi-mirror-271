from pathlib import Path

source_root = Path(__file__).parent.resolve() / "cast_vue" / "static" / "src"

source_files = []
extensions = {".ts", ".vue"}
for path in source_root.rglob("*"):
    if "test" in path.name:
        continue
    if path.suffix in extensions:
        name = f"{path.parent.name}/{path.name}"
        # print(name)
        with path.open("r") as f:
            content = f.read()
        source_files.append((name, content))

contents = []
for name, source in source_files:
    contents.append(f"// file named {name}")
    contents.append(source)
source_content = "\n".join(contents)
print(source_content)
