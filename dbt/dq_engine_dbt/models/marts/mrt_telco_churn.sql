select
  *,
  case when lower(cast(churn as varchar)) in ('yes','1','true') then 1 else 0 end as churn_flag
from {{ ref('stg_telco') }}
