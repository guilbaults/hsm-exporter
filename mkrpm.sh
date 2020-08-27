#!/bin/bash
spectool -g -R hsm-exporter-el7.spec
rpmbuild --define "dist .el7" -ba hsm-exporter-el7.spec
