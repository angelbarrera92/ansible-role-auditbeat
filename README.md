# Ansible Role: Auditbeat

![Auditbeat](./.assets/auditbeat.png)

An Ansible Role that installs Auditbeat on RedHat/CentOS or Debian/Ubuntu.

> Auditbeat is a lightweight shipper that you can install on your servers to audit the activities of users and processes on your systems. For example, you can use Auditbeat to collect and centralize audit events from the Linux Audit Framework. You can also use Auditbeat to detect changes to critical files, like binaries and configuration files, and identify potential security policy violations.

source: [https://www.elastic.co/guide/en/beats/auditbeat/6.x/auditbeat-overview.html](https://www.elastic.co/guide/en/beats/auditbeat/6.x/auditbeat-overview.html)

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
auditbeat_create_config: true
```

Whether to create the Auditbeat configuration file and handle the copying of SSL key and cert for auditbeat. If you prefer to create a configuration file yourself you can set this to `false`.

```yaml
auditbeat_modules_conf:
  - module: file_integrity
    paths:
      - /bin
      - /usr/bin
      - /sbin
      - /usr/sbin
      - /etc
    exclude_files:
      - '(?i)\.sw[nop]$'
      - '~$'
      - '/\.git($|/)'
    scan_at_start: true
    scan_rate_per_sec: 50 MiB
    max_file_size: 100 MiB
    hash_types: [sha256]
    recursive: false
  - module: auditd
    resolve_ids: true
    failure_mode: silent
    backlog_limit: 8192
    rate_limit: 0
    include_raw_message: false
    include_warnings: false
    backpressure_strategy: auto
```

Modules configuration that will be listed in the `auditbeat.modules` section of the Auditbeat configuration file. Read through the [Auditbeat modules configuration guide](https://www.elastic.co/guide/en/beats/auditbeat/6.x/auditbeat-modules.html) for more options.

```yaml
auditbeat_output_logstash_enabled: true
auditbeat_output_logstash_hosts:
  - "localhost:5044"
```

Whether to enable Logstash output, and which hosts to send output to.

```yaml
auditbeat_enable_processors: true
auditbeat_processors_conf:
  - add_host_metadata: ~
```

Whether to enable processors, and which one use. How to define processors can be found [here](https://www.elastic.co/guide/en/beats/auditbeat/current/defining-processors.html)

```yaml
auditbeat_enable_logging: false
auditbeat_log_level: warning
auditbeat_log_dir: /var/log/auditbeat
auditbeat_log_filename: auditbeat.log
```

Auditbeat logging.


```yaml
auditbeat_ssl_dir: /etc/pki/logstash
```

The path where certificates and keyfiles will be stored.

```yaml
auditbeat_ssl_certificate_file: ""
auditbeat_ssl_key_file: ""
```

Local paths to the SSL certificate and key files, which will be copied into the `auditbeat_ssl_dir`.

For utmost security, you should use your own valid certificate and keyfile, and update the `auditbeat_ssl_*` variables in your playbook to use your certificate.

To generate a self-signed certificate/key pair, you can use use the command:

```bash
sudo openssl req -x509 -batch -nodes -days 3650 -newkey rsa:2048 -keyout auditbeat.key -out auditbeat.crt
```

Note that auditbeat and logstash may not work correctly with self-signed certificates unless you also have the full chain of trust (including the Certificate Authority for your self-signed cert) added on your server. See: [https://github.com/elastic/logstash/issues/4926#issuecomment-203936891](https://github.com/elastic/logstash/issues/4926#issuecomment-203936891)

```yaml
auditbeat_ssl_insecure: "false"
```

Set this to `"true"` to allow the use of self-signed certificates (when a CA isn't available).

## Dependencies

None.

## Example Playbook

```yaml
    - hosts: all
      roles:
        - role: auditbeat
          stop_service_auditd: false
          auditbeat_modules_conf:
            - module: file_integrity
              paths:
                - /bin
                - /usr/bin
                - /sbin
                - /usr/sbin
                - /etc
              exclude_files:
                - '(?i)\.sw[nop]$'
                - '~$'
                - '/\.git($|/)'
              scan_at_start: true
              scan_rate_per_sec: 50 MiB
              max_file_size: 100 MiB
              hash_types: [sha256]
              recursive: false
            - module: auditd
              resolve_ids: true
              failure_mode: silent
              backlog_limit: 8192
              rate_limit: 0
              include_raw_message: false
              include_warnings: false
              backpressure_strategy: auto
          auditbeat_enable_logging: true
          auditbeat_log_level: debug
```

## License

MIT

## Author Information

This role has been created in 2018 by [Ángel Barrera](https://github.com/angelbarrera92).
