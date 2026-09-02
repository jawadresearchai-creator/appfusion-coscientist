package main

import (
    "archive/zip"
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
    "errors"
    "fmt"
    "io"
    "os"
    "path"
    "path/filepath"
    "strings"
    "unicode"
)

const (
    maxEntries            = 200000
    maxEntryNameBytes     = 1024
    maxEntryUncompressed  = uint64(2 << 30)
    maxTotalUncompressed  = uint64(8 << 30)
)

type Inventory struct {
    SchemaVersion      string   `json:"schema_version"`
    ContainerKind      string   `json:"container_kind"`
    FileName           string   `json:"file_name"`
    SHA256             string   `json:"sha256"`
    SizeBytes          int64    `json:"size_bytes"`
    EntryCount         int      `json:"entry_count"`
    TotalUncompressed  uint64   `json:"total_uncompressed_bytes"`
    HasAndroidManifest bool     `json:"has_android_manifest"`
    DexFiles           []string `json:"dex_files"`
    NativeLibraries    []string `json:"native_libraries"`
    ResourceArchives   []string `json:"resource_archives"`
    NestedAPKs         []string `json:"nested_apks"`
}

func containerKind(name string) (string, error) {
    switch strings.ToLower(filepath.Ext(name)) {
    case ".apk":
        return "APK", nil
    case ".apkm":
        return "APKM", nil
    case ".xapk":
        return "XAPK", nil
    default:
        return "", errors.New("unsupported container extension")
    }
}

func isDriveAbsolute(name string) bool {
    if len(name) < 2 || name[1] != ':' {
        return false
    }
    return unicode.IsLetter(rune(name[0]))
}

func validateEntry(f *zip.File) error {
    name := f.Name
    if name == "" {
        return errors.New("empty ZIP entry name")
    }
    if len(name) > maxEntryNameBytes {
        return fmt.Errorf("ZIP entry name exceeds %d bytes", maxEntryNameBytes)
    }
    if strings.ContainsRune(name, '\x00') || strings.Contains(name, "\\") {
        return fmt.Errorf("unsafe ZIP entry path %q", name)
    }
    if strings.HasPrefix(name, "/") || isDriveAbsolute(name) {
        return fmt.Errorf("absolute ZIP entry path %q", name)
    }
    trimmed := strings.TrimSuffix(name, "/")
    cleaned := path.Clean(trimmed)
    if cleaned == "." || cleaned == ".." || strings.HasPrefix(cleaned, "../") || cleaned != trimmed {
        return fmt.Errorf("non-canonical ZIP entry path %q", name)
    }
    mode := f.Mode()
    if mode&os.ModeSymlink != 0 {
        return fmt.Errorf("symlink ZIP entry rejected: %q", name)
    }
    if mode&os.ModeType != 0 && !mode.IsDir() {
        return fmt.Errorf("special ZIP entry rejected: %q", name)
    }
    if f.UncompressedSize64 > maxEntryUncompressed {
        return fmt.Errorf("ZIP entry %q exceeds uncompressed-size limit", name)
    }
    return nil
}

func hashFile(file *os.File) (string, error) {
    if _, err := file.Seek(0, io.SeekStart); err != nil {
        return "", err
    }
    digest := sha256.New()
    if _, err := io.Copy(digest, file); err != nil {
        return "", err
    }
    return hex.EncodeToString(digest.Sum(nil)), nil
}

func inspect(input string) (*Inventory, error) {
    kind, err := containerKind(input)
    if err != nil {
        return nil, err
    }
    file, err := os.Open(input)
    if err != nil {
        return nil, err
    }
    defer file.Close()

    stat, err := file.Stat()
    if err != nil {
        return nil, err
    }
    if stat.Size() <= 0 {
        return nil, errors.New("input is empty")
    }
    digest, err := hashFile(file)
    if err != nil {
        return nil, err
    }
    reader, err := zip.NewReader(file, stat.Size())
    if err != nil {
        return nil, fmt.Errorf("invalid ZIP-structured package: %w", err)
    }
    if len(reader.File) == 0 || len(reader.File) > maxEntries {
        return nil, fmt.Errorf("entry count outside allowed range: %d", len(reader.File))
    }

    inventory := &Inventory{
        SchemaVersion: "1.0.0",
        ContainerKind: kind,
        FileName:      filepath.Base(input),
        SHA256:        digest,
        SizeBytes:     stat.Size(),
        EntryCount:    len(reader.File),
        DexFiles:      []string{},
        NativeLibraries: []string{},
        ResourceArchives: []string{},
        NestedAPKs:    []string{},
    }

    for _, entry := range reader.File {
        if err := validateEntry(entry); err != nil {
            return nil, err
        }
        if inventory.TotalUncompressed > maxTotalUncompressed-entry.UncompressedSize64 {
            return nil, errors.New("package exceeds total uncompressed-size limit")
        }
        inventory.TotalUncompressed += entry.UncompressedSize64
        name := entry.Name
        switch {
        case name == "AndroidManifest.xml":
            inventory.HasAndroidManifest = true
        case strings.HasPrefix(name, "classes") && strings.HasSuffix(name, ".dex") && !strings.Contains(name, "/"):
            inventory.DexFiles = append(inventory.DexFiles, name)
        case strings.HasPrefix(name, "lib/") && strings.HasSuffix(name, ".so"):
            inventory.NativeLibraries = append(inventory.NativeLibraries, name)
        case name == "resources.arsc":
            inventory.ResourceArchives = append(inventory.ResourceArchives, name)
        case strings.HasSuffix(strings.ToLower(name), ".apk"):
            inventory.NestedAPKs = append(inventory.NestedAPKs, name)
        }
    }
    return inventory, nil
}

func main() {
    if len(os.Args) != 3 {
        fmt.Fprintln(os.Stderr, "usage: static-apk-inventory <input.apk|apkm|xapk> <output.json>")
        os.Exit(2)
    }
    inventory, err := inspect(os.Args[1])
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(3)
    }
    encoded, err := json.MarshalIndent(inventory, "", "  ")
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(4)
    }
    encoded = append(encoded, '\n')
    if err := os.WriteFile(os.Args[2], encoded, 0644); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(5)
    }
}
