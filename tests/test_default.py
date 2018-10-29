import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]).get_hosts("all")


def test_packages(host):
    """Test packages installation."""
    assert host.package("auditbeat").is_installed


def test_filebeat_file(host):
    """Test the filebeat configuration file exists."""
    assert host.file("/etc/auditbeat/auditbeat.yml").exists


def test_filebeat_file_contains_config(host):
    """Test the filebeat configuration file contains a current value."""
    assert "scan_at_start" in host.file(
        "/etc/auditbeat/auditbeat.yml").content_string


def test_filebeat_file_contains_logstash_config(host):
    """Test the filebeat configuration file contains logstash default value."""
    assert "localhost:5044" in host.file(
        "/etc/auditbeat/auditbeat.yml").content_string


def test_filebeat_file_contains_tags_config(host):
    """Test the filebeat configuration file contains logstash default value."""
    assert "tags: [\"auditbeat\"]" in host.file(
        "/etc/auditbeat/auditbeat.yml").content_string
