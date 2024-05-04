# Krypt: GitOps-friendly Secret Management for Kubernetes Clusters

Krypt is a tool designed to streamline secret management within Kubernetes cluster (and pretty much any other) configurations, particularly suited for GitOps workflows. It enables users to securely seal and unseal secrets within cluster configuration folders, ensuring sensitive information remains protected both in transit and at rest.

## Getting Started

To begin using Krypt, follow these simple steps:

1. **Initialization**: Initialize the cluster directory using the `krypt init` command. Provide a passphrase for encryption and specify the path to the cluster directory.
   
    ```bash
    krypt init --passphrase PASSPHRASE /path/to/cluster
    ```

2. **Sealing Secrets**: Seal the secrets within the cluster directory using the `krypt seal` command.

    ```bash
    krypt seal /path/to/cluster
    ```

3. **Commit and Push**: Once sealed, commit the changes to your Git repository and push them upstream. This ensures that the encrypted secrets are securely stored and version controlled.

4. **CI/CD Integration**: In your CI/CD pipeline, use the `krypt unseal` command to unseal the secrets before applying manifests onto the cluster. Pass the passphrase for decryption and specify the path to the cluster directory.

    ```bash
    krypt unseal --passphrase PASSPHRASE /path/to/cluster
    ```

## Usage Guidelines

- Only files with `.kpt.` in the name or those ending with `.kpt` are sealed by Krypt. Other files within the cluster directory remain stored in plaintext. This ensures that only intended secrets are encrypted while maintaining transparency for other configuration files.

- Krypt automatically adds files with `.kpt.` in the name or those ending with `.kpt` to .gitignore to ensure that plaintext secrets are not being committed to the repository.

- It's essential to securely manage and store the passphrase used for sealing and unsealing secrets. Consider using secure key management practices to protect this passphrase.

## Contributing

Contributions to Krypt are welcome! Feel free to open issues for bug reports, feature requests, or any questions you may have. Pull requests are also encouraged for those who would like to contribute directly to the project's development.

## License

Krypt is licensed under the [GPLv3 License](LICENSE), allowing for both personal and commercial use with proper attribution. Refer to the license file for detailed information.

## Acknowledgments

Krypt was inspired by the need for a secure and streamlined approach to managing secrets within Kubernetes clusters, particularly in GitOps workflows. We extend our gratitude to the open-source community for their contributions and support.

---

**Krypt** - Secure Secret Management for Kubernetes Clusters

For more information, visit [Krypt on GitHub](https://github.com/kubertools/krypt)
