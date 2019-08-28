-- Create a view for querying a question's details
CREATE VIEW question_details_view AS
(SELECT
    q.id id,
    q.description question,
    q.created_by created_by_q,
    q.created_at created_at_q,
    a.id answer_id,
    a.description answer,
    a.created_by created_by_a,
    a.created_at created_at_a,
    c.name category
FROM
    questions q
    LEFT JOIN answers a ON q.id = a.question
    LEFT JOIN categories c ON q.category = c.id);

/*
Running EXPLAIN for the query with the above view shows that the query
was executed for a short time and primary key indexes were used for index scans
*/
EXPLAIN ANALYZE (SELECT * FROM question_details_view WHERE id=1);

/*
Nested Loop Left Join  (cost=0.15..21.35 rows=1 width=986) (actual time=0.032..0.034 rows=1 loops=1)
  ->  Nested Loop Left Join  (cost=0.00..13.15 rows=1 width=872) (actual time=0.021..0.022 rows=1 loops=1)
        Join Filter: (q.id = a.question)
        ->  Seq Scan on questions q  (cost=0.00..1.01 rows=1 width=438) (actual time=0.013..0.013 rows=1 loops=1)
              Filter: (id = 1)
        ->  Seq Scan on answers a  (cost=0.00..12.12 rows=1 width=438) (actual time=0.004..0.005 rows=1 loops=1)
              Filter: (question = 1)
  ->  Index Scan using categories_pkey on categories c  (cost=0.15..8.17 rows=1 width=122) (actual time=0.009..0.009 rows=1 loops=1)
        Index Cond: (q.category = id)
Planning Time: 0.197 ms
Execution Time: 0.067 ms
*/


-- Running EXPLAIN for a question search
EXPLAIN ANALYZE (SELECT * FROM questions WHERE LOWER(description) LIKE LOWER('%Python%'));

/*
Seq Scan on questions  (cost=0.00..1.01 rows=1 width=446) (actual time=0.012..0.013 rows=1 loops=1)
  Filter: (lower((description)::text) ~~ '%python%'::text)
Planning Time: 0.065 ms
Execution Time: 0.026 ms
*/

-- Creating an index on description and re-running explain shows that the index is skipped
CREATE INDEX idx_questions_description ON questions (description);
