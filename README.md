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
Some property values (s.g. `color`, `style` and `logo`) are following it.

### Document

See `/shields/docs` for detail.

### quick document (2022/02/06)

- `/shields?label=${LABEL}&message=${MESSAGE}&color=${OPTION:COLOR}&style=${OPTION:STYLE}&logo=${OPTION:LOGO}`
    - FreeStyle Badge
    - ![](http://s.cympfh.cc/shields?label=Build&message=failed&color=red&style=flat-square&logo=circleci)
    - ![](http://s.cympfh.cc/shields?label=+&message=cympfh&style=flat-square&logo=twitch&color=gray&labelColor=gray&logoColor=white)
    - ![](http://s.cympfh.cc/shields?label=+&message=cympfh&style=flat-square&logo=twitter&color=gray&labelColor=gray&logoColor=white)
- `/shields/atcoder/rating?username=${username}`
    - Latest Rating in AtCoder
    - ![](http://s.cympfh.cc/shields/atcoder/rating?username=cympfh&style=flat-square)
- `/shields/codeforces/rating?username=${username}`
    - Latest Rating in Codeforces
    - **This API takes slowly**
    - ![](http://s.cympfh.cc/shields/codeforces/rating?username=cympfh&style=flat-square)
- `/shields/speedrun/place?username=${username}&gamename=${gamename}`
    - Your Best Place
    - ![](http://s.cympfh.cc/shields/speedrun/place?username=cympfh&gamename=katamarireroll&style=flat-square)
- `/shields/speedrun/realtime?username=${username}&gamename=${gamename}`
    - Your Best Time
    - ![](http://s.cympfh.cc/shields/speedrun/realtime?username=cympfh&gamename=katamarireroll&style=flat-square)
