import os
import subprocess

# MB size threshold
SIZE_LIMIT_MB = 100
SIZE_LIMIT_BYTES = SIZE_LIMIT_MB * 1024 * 1024

def get_git_files():
    result = subprocess.run(['git', 'ls-files'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().split('\n')

def find_large_files():
    large_files = []
    files = get_git_files()

    for file in files:
        try:
            size = os.path.getsize(file)
            if size > SIZE_LIMIT_BYTES:
                large_files.append((file, round(size / (1024 * 1024), 2)))  # in MB
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")
            continue

    return large_files

if __name__ == '__main__':
    print(f"🔍 Scanning for files over {SIZE_LIMIT_MB}MB...\n")
    large_files = find_large_files()

    if large_files:
        print(f"⚠️ Found {len(large_files)} large files:")
        for f, s in large_files:
            print(f"{f} — {s} MB")
    else:
        print("✅ No large files found!")
