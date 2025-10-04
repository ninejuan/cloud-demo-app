## Cloud Demo App
---
클라우드컴퓨팅 학습 시 사용하기 위한 Demo App 모음입니다.

### App Lists
- Product (use DynamoDB)
- User (use RDS MySQL)
- Stress (CPU Stress app)
- Green (use RDS postgreSQL)
- Red (use RDS MySQL)
- HelloWorld (only Fixed Responses)

## Docker Repositories

### Repository URLs
- **Product App**: `juanylee/demo-product`
- **User App**: `juanylee/demo-user`
- **Stress App**: `juanylee/demo-stress`
- **Green App**: `juanylee/demo-green`
- **Red App**: `juanylee/demo-red`
- **HelloWorld App**: `juanylee/helloworld`

### Usage
```bash
# Pull latest image
docker pull juanylee/demo-product:latest

# Run container
docker run -p 8080:8080 juanylee/demo-product:latest

# Run with specific version
docker run -p 8080:8080 juanylee/demo-product:1.0.0
```

## API Specs

### Product App
| Path | Method | Request (example) | Response Code | Response Body |
|------|--------|-------------------|---------------|---------------|
| `/v1/product` | POST | `{"requestid": "999999999999", "uuid": "7c5a3c6a-758f-4bc5-9bdf-3e573a0ad729", "id": "dbdump500001", "name": "dbdump500001", "price": 1234}` | 201 | `{"status": "created", "id": "dbdump500001"}` |
| `/v1/product` | GET | `?id=dbdump500001&requestid=999999999999&uuid=7c5a3c6a-758f-4bc5-9bdf-3e573a0ad729` | 200 | `{"id": "dbdump500001", "name": "dbdump500001", "price": 1234}` |
| `/healthcheck` | GET | - | 200 | `{"status": "ok"}` |

### User App
| Path | Method | Request (example) | Response Code | Response Body |
|------|--------|-------------------|---------------|---------------|
| `/v1/user` | POST | `{"requestid": "999999999999", "uuid": "7c5a3c6a-758f-4bc5-9bdf-3e573a0ad729", "username": "dbdump500001", "email": "dbdump500001@example.org", "status_message": "I'm happy"}` | 201 | `{"status": "created", "email": "dbdump500001@example.org"}` |
| `/v1/user` | GET | `?email=dbdump500001@example.org&requestid=999999999999&uuid=7c5a3c6a-758f-4bc5-9bdf-3e573a0ad729` | 200 | `{"username": "dbdump500001", "email": "dbdump500001@example.org", "status_message": "I'm happy"}` |
| `/healthcheck` | GET | - | 200 | `{"status": "ok"}` |

### Stress App
| Path | Method | Request (example) | Response Code | Response Body |
|------|--------|-------------------|---------------|---------------|
| `/v1/stress` | POST | `{"requestid": "999999999999", "uuid": "7c5a3c6a-758f-4bc5-9bdf-3e573a0ad729", "length": 256}` | 201 | `{"status": "completed", "length": 256}` |
| `/healthcheck` | GET | - | 200 | `{"status": "ok"}` |

### Green App
| Path | Method | Request (example) | Response Code | Response Body |
|------|--------|-------------------|---------------|---------------|
| `/health` | GET | - | 200 | `200 OK` |
| `/green` | POST | `{"x": "abcd", "y": 21}` | 200 | `{"status": "inserted", "id": "xx11abcd"}` |
| `/green` | GET | `?id=xx11abcd` | 200 | `{"x": "abcd", "y": 21, "version": "1.0.0"}` |

### Red App
| Path | Method | Request (example) | Response Code | Response Body |
|------|--------|-------------------|---------------|---------------|
| `/health` | GET | - | 200 | `200 OK` |
| `/red` | POST | `{"name": "kim"}` | 200 | `{"status": "inserted", "id": "yy11abcd"}` |
| `/red` | GET | `?id=yy11abcd` | 200 | `{"name": "kim", "version": "1.0.0"}` |

### HelloWorld App
| Path | Method | Request (example) | Response Code | Response Body |
|------|--------|-------------------|---------------|---------------|
| `/` | GET | - | 200 | `Hello World!` |
| `/health` | GET | - | 200 | `{"status": "ok"}` |
| `/time` | GET | - | 200 | `{"timestamp": "2025-01-27T10:30:00Z"}` |
| `/ver` | GET | - | 200 | `{"version": "1.0.0"}` |

## Copyrights
- Green, Red 2025년도 전국기능경기대회 1과제 어플리케이션 Spec을 참고하여 개발하였습니다.
- Product, user, stress App은 2025년도 전국기능경기대회 3과제 어플리케이션 Spec을 참고하여 개발하였습니다.