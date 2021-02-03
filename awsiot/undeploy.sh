region=ap-east-1
certificateId=$(cat "deepracer/certs/certificateId.txt")
echo $certificateId

aws iot update-certificate \
    --region $region \
    --certificate-id $certificateId \
    --new-status INACTIVE

aws iot delete-certificate \
    --region $region \
    --certificate-id $certificateId \
    --force-delete
    
aws cloudformation delete-stack --stack-name awsiotdeepracer --region $region