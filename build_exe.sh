#!/bin/zsh

echo "Using pyinstaller:"
echo $(which pyinstaller)

# Dynamically generate the list of hidden imports
HIDDEN_IMPORTS=()
for file in az/*_provider.py; do
    module=$(basename "$file" .py)
    HIDDEN_IMPORTS+=(--hidden-import "az.$module")
done

# Print the hidden imports for debugging
echo "Hidden imports: ${HIDDEN_IMPORTS[@]}"

# Build the project using --onedir
pyinstaller --noconfirm --clean \
    az/az.py \
    ${HIDDEN_IMPORTS[@]}

# Verify the build output
if [[ ! -d "dist/az" ]]; then
    echo "Error: dist/az not found"
    exit 1
fi

# Move the entire directory to a safe location
INSTALL_DIR="$HOME/.local/share/az"
mkdir -p "$INSTALL_DIR"
rm -rf "$INSTALL_DIR"
mv dist/az "$INSTALL_DIR"

# Create a wrapper script in $HOME/.local/bin
WRAPPER="$HOME/.local/bin/az"
cat <<EOF > "$WRAPPER"
#!/bin/bash
exec "$INSTALL_DIR/az" "\$@"
EOF

chmod +x "$WRAPPER"
echo "Installed to $WRAPPER"