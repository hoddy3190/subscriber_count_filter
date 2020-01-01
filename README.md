# subscriber_count_filter

## Youtube Data APIのつらみポイント

+ publishedAfter: 2019-01-01T00:00:00Z
  - publishedAfterがよくわからん
  - type: channelを指定する。そうすると結果がチャンネル登録日が2019年1月1日以降のものに絞られることを期待するがそうならない。
+ location
  - 37.42307,-122.08427と指定し、locationRadiusとセットで使うと地域が絞られるが、typeがvideoのときのみ有効（typeをvideoにしないとエラーになる）
  - 現状、「地域」を絞るサーチクエリはない
