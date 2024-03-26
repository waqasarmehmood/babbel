
module "s3" {
  source = "../../modules/s3"

  s3_bucket_parameters = {
    bucket1 = {
      s3_bucket = "s3-datalake-${local.enviroment}-raw"
      tags = {
        environment = local.enviroment
        layer       = "raw"
      }
    }

    bucket2 = {
      s3_bucket = "s3-datalake-${local.enviroment}-staging"
      tags = {
        environment = local.enviroment
        layer       = "staging"
      }
    }

    bucket3 = {
      s3_bucket = "s3-datalake-${local.enviroment}-adl"
      tags = {
        environment = local.enviroment
        layer       = "prod"
      }
    }
  }
}