# docker-ceph-demo
using ceph-demo image

# Launch
```
$ docker-compose up -d
```

## Create radosgw user
```
(in ceph_ceph_1)$ radosgw-admin user create --uid=testuser --display-name="First User"
```
