select
  *
from {{ source('raw', 'telco') }}
