resource "aws_s3_bucket" "this" {
  for_each   = var.s3_bucket_parameters
  bucket     = each.value.s3_bucket

  tags = merge(each.value.tags, {
    Name : each.key
  })
}