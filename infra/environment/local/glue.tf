resource "aws_iam_role" "glue" {
  name = "AWSGlueServiceRoleDefault"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "glue_service" {
    role = "${aws_iam_role.glue.id}"
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy" "glue_s3_write_policy" {
    name   = "glue_s3_write_policy"
    role   = aws_iam_role.glue.id
    policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
              "arn:aws:s3:::s3-datalake-${local.enviroment}-raw",
              "arn:aws:s3:::s3-datalake-${local.enviroment}-raw/*",
              "arn:aws:s3:::s3-datalake-${local.enviroment}-staging",
              "arn:aws:s3:::s3-datalake-${local.enviroment}-staging/*",
              "arn:aws:s3:::s3-datalake-${local.enviroment}-adl",
              "arn:aws:s3:::s3-datalake-${local.enviroment}-adl/*"
      ]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "glue_assume_role_for_kinesis" {
    name = "glue_assume_role_for_kinesis"
    role = "${aws_iam_role.glue.id}"
    policy = <<EOF
{
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect"   : "Allow",
        "Action"   : "sts:AssumeRole",
        "Resource" : [
            "${local.kinesis_cross_account}"
            ]
    }]
  }
EOF
}