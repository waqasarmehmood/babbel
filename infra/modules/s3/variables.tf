
variable "s3_bucket_parameters" {
  description = "S3 parameters"
  type = map(object({
    s3_bucket   = string
    tags       = optional(map(string), {})
  }))
  default = {}
}