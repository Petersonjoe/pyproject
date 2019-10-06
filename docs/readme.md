## This is a Read Me placeholder

***This folder aims to stores related documentations for the project/tools***

### Section 1: List of the info

The goal of this project is to get some data from douban.com and to take some examples for data analysis - from raw data acquiring, data cleaning, to data analyzing.

##### URL List Analysis

> TV list in head page

|Objective|Detail|
|:---|:---|
|WEB\_SUBJECT|最近热门电视剧|
|TV\_LIST\_URL|https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0|
|RESPONSE|directly click above link or see [tv_response.json](./weixin/tv_response.html)|
|SAMPLE|see below sample|

A sample - **致命女人**:

  ```json
{
  "rate": "9.3",
  "cover_x": 1236,
  "title": "致命女人",
  "url": "https://movie.douban.com/subject/30401122/",
  "playable": false,
  "cover": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2566967861.jpg",
  "id": "30401122",
  "cover_y": 1824,
  "is_new": false
}
  ```

> Child pages

From above sample, you can got 2 sub URLs:

- URL of the TV's home page `https://movie.douban.com/subject/30401122/`, and you can fetch below page with it.
- URL of the TV's icon: `https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2566967861.jpg`
  ![致命女人](./imgs/why_women_kill.png)

Search the url: https://movie.douban.com/subject/30401122/, you will got response:

- header: https://movie.douban.com/subject/30401122/comments?status=P
- comment page: see tv\_comment\_response\_page1.html
- the page navigator:

	```html
	<a href="?start=0&amp;limit=20&amp;sort=new_score&amp;status=P&amp;percent_type=" data-page="1"><< 首页</a>
	<a href="?start=19&amp;limit=-20&amp;sort=new_score&amp;status=P&amp;percent_type=" data-page="">< 前页</a>
	<a href="?start=40&amp;limit=20&amp;sort=new_score&amp;status=P&amp;percent_type=" data-page="" class="next">后页 ></a>
	```
	
Then you can try this query: 
	
	https://movie.douban.com/subject/30401122/comments?start=40&limit=20&sort=new_score&status=P&percent_type=

While, no matter how to adjust the parameters, each time the page will only response 20 comments. This is a point to dive into but takes much time is worthless.

Then, need to parse the html to get the scores.

--
### Next section: Analysis for movie list
--


㊗️㊗️㊗️🇨🇳🇨🇳🇨🇳🇨🇳🇨🇳🇨🇳🇨🇳㊗️㊗️㊗️
### ***Previous: List of info***
***

> Movies list in head page

|Objective|Detail|
|:---|:---|
|WEB\_SUBJECT|最近热门电影|
|MOVIE\_LIST\_URL|https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0|
|RESPONSE|directly click above link or see [movie_response.json](./weixin/movie_response.json)|
|SAMPLE|see below sample|

A sample - ***极限逃生***:
	
```json
{
  "rate": "7.8",
  "cover_x": 1000,
  "title": "极限逃生",
  "url": "https://movie.douban.com/subject/30210691/",
  "playable": false,
  "cover": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2563546656.jpg",
  "id": "30210691",
  "cover_y": 1425,
  "is_new": false
},
```

> Child page

Search the URL: `https://movie.douban.com/subject/30210691/` you will got response:

 - got comment html: see [movie_comment_response_page.html](./wenxin/movie_comment_response_page1.html)
 - the page navigator:

```html
<div id="paginator" class="center">
    <span class="first"><< 首页</span>
    <span class="prev">< 前页</span>
    <a href="?start=20&amp;limit=20&amp;sort=new_score&amp;status=P&amp;percent_type=" data-page="" class="next">后页 ></a>
</div>
```

Similar as for TVs, the url to navigate each page is using below url:

	https://movie.douban.com/subject/30210691/comments?start=0&limit=20&sort=new_score&status=P&percent_type=

> ### ***Next: Start crawling the TV and Movies***






