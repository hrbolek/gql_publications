from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createInsertQuery,
    createQueryTest
)

test_plan_by_id = createByIdTest(tableName="plans")
test_plan_page = createPageTest(tableName="plans")
test_plan_insert = createInsertQuery(tableName="plans")
test_plan_coverage = createQueryTest(tableName="plans", queryName="coverage")
test_plan_update = createUpdateQuery(tableName="plans")

test_plan_lesson_by_id = createByIdTest(tableName="plan_lessons")
test_plan_lesson_page = createPageTest(tableName="plan_lessons")
test_plan_lesson_insert = createInsertQuery(tableName="plan_lessons")
test_plan_lesson_update = createUpdateQuery(tableName="plan_lessons")

test_plan_lesson_coverage_mutations = createQueryTest(tableName="plan_lessons", queryName="coveragemutation")