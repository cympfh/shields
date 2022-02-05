# shields

Shields API

## Deployment

All in `Dockerfile` and `Makefile`.
You should just do,

```bash
$ make run  # docker build & run, PORT=8080 by default

$ make run PORT=9999
```

## API

This is a just proxy of [Shields.io](https://shields.io/).
Some property values (s.g. `color`) are following it.

### Document

See `/docs` for detail.

### quick document (2022/02/06)

- `/shields/atcoder/rating?username=${username}`
    - Latest Rating in AtCoder
- `/shields/codeforces/rating?username=${username}`
    - Latest Rating in Codeforces
    - This API takes slowly
- `/shields/speedrun/place?username=${username}&gamename=${gamename}`
    - Your Best Place
- `/shields/speedrun/realtime?username=${username}&gamename=${gamename}`
    - Your Best Time
