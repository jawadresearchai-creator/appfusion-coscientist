package main

import (
    "encoding/json"
    "fmt"
    "net"
    "os"
    "strings"
    "time"
)

type ProbeResult struct {
    SchemaVersion         string   `json:"schema_version"`
    PublicNetworkBlocked  bool     `json:"public_network_blocked"`
    MetadataNetworkBlocked bool    `json:"metadata_network_blocked"`
    SensitiveEnvironment []string `json:"sensitive_environment"`
}

func blocked(address string) bool {
    connection, err := net.DialTimeout("tcp", address, 2*time.Second)
    if err != nil {
        return true
    }
    _ = connection.Close()
    return false
}

func sensitiveEnvironment() []string {
    findings := []string{}
    for _, item := range os.Environ() {
        key := item
        if index := strings.IndexByte(item, '='); index >= 0 {
            key = item[:index]
        }
        upper := strings.ToUpper(key)
        if strings.Contains(upper, "TOKEN") || strings.Contains(upper, "SECRET") ||
            strings.HasPrefix(upper, "AWS_") || strings.HasPrefix(upper, "AZURE_") ||
            strings.HasPrefix(upper, "GOOGLE_") || strings.HasPrefix(upper, "ACTIONS_ID_TOKEN_") ||
            upper == "GITHUB_TOKEN" {
            findings = append(findings, key)
        }
    }
    return findings
}

func main() {
    result := ProbeResult{
        SchemaVersion:          "1.0.0",
        PublicNetworkBlocked:   blocked("1.1.1.1:443"),
        MetadataNetworkBlocked: blocked("169.254.169.254:80"),
        SensitiveEnvironment:   sensitiveEnvironment(),
    }
    encoded, err := json.MarshalIndent(result, "", "  ")
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(2)
    }
    fmt.Println(string(encoded))
    if !result.PublicNetworkBlocked || !result.MetadataNetworkBlocked || len(result.SensitiveEnvironment) != 0 {
        os.Exit(3)
    }
}
