from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address= models.CharField(max_length=3000)
    gender= models.CharField(max_length=30)

class ddos_attacks_prediction(models.Model):


    RID= models.CharField(max_length=3000)
    Protocol= models.CharField(max_length=3000)
    ip_src= models.CharField(max_length=3000)
    ip_dst= models.CharField(max_length=3000)
    pro_srcport= models.CharField(max_length=3000)
    pro_dstport= models.CharField(max_length=3000)
    flags_ack= models.CharField(max_length=3000)
    ip_flags_mf= models.CharField(max_length=3000)
    ip_flags_df= models.CharField(max_length=3000)
    ip_flags_rb= models.CharField(max_length=3000)
    pro_seq= models.CharField(max_length=3000)
    pro_ack= models.CharField(max_length=3000)
    frame_time= models.CharField(max_length=3000)
    Packets= models.CharField(max_length=3000)
    Bytes1= models.CharField(max_length=3000)
    Tx_Packets= models.CharField(max_length=3000)
    Tx_Bytes= models.CharField(max_length=3000)
    Rx_Packets= models.CharField(max_length=3000)
    Rx_Bytes= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



