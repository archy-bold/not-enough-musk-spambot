-- All time top comment
select * from comments order by score desc limit 25;

-- Last 28 days top comments
select * from comments where commented_at > datetime('now', '-28 days') order by score desc limit 25;

-- All time best performing comments
select body, sum(score) / count(*) as agg_score, count(*) as num_comments from comments group by body having num_comments> 4 order by agg_score desc limit 25;

-- Last 28 days best performing comments
select body, sum(score) / count(*) as agg_score, count(*) as num_comments from comments where commented_at > datetime('now', '-28 days') group by body order by agg_score desc limit 25;

-- All time worst performing comments
select body, sum(score) / count(*) as agg_score, count(*) as num_comments from comments group by body having num_comments > 4 order by agg_score asc, num_comments desc limit 25;

-- Last 28 days worst performing comments
select body, sum(score) / count(*) as agg_score, count(*) as num_comments from comments where commented_at > datetime('now', '-28 days') group by body order by agg_score asc, num_comments desc limit 25;

-- All time worst performing comments with at least 5 posts
select body, sum(score) / count(*) as agg_score, count(*) as num_comments from comments group by body having num_comments > 4 order by agg_score asc limit 25;

-- Last 28 days worst performing comments with at least 5 posts
select body, sum(score) / count(*) as agg_score, count(*) as num_comments from comments where commented_at > datetime('now', '-28 days') group by body having num_comments > 4 order by agg_score asc limit 25;

-- All time most commented
select body, sum(score) / count(*) as agg_score, count(*) as num_comments from comments group by body order by num_comments desc limit 25;

-- Last 28 days most commented
select body, sum(score) / count(*) as agg_score, count(*) as num_comments from comments where commented_at > datetime('now', '-28 days') group by body order by num_comments desc limit 25;

-- All time worst comments
select * from comments order by score asc limit 25;

-- Last 28 days worst comments
select * from comments where commented_at > datetime('now', '-28 days') order by score asc limit 25;
