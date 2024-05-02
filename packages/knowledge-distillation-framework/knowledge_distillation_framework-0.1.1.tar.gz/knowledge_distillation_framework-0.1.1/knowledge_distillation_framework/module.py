import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as L
from torch import optim

def logit_distillation_loss(student_logits, teacher_logits, temperature=1.0):
    '''
    Compute the KL divergence loss between the student and teacher logits.
    TODO: TEST
    '''
    return F.kl_div(F.log_softmax(student_logits / temperature, dim=1), F.softmax(teacher_logits / temperature, dim=1))

class KnowledgeDistillationModule(L.LightningModule):
    '''
    A PyTorch Lightning module for knowledge distillation.

    The student encoder and teacher encoder should output the same feature dimension.
    
    The task loss function takes arguments (zs, zt, qs, qt, y) where zs and zt 
    are the student and teacher embeddings, qs and qt are the student and teacher
    head outputs, and y is the targets for the dataset.

    The encoder heads are applied to the output of the encoders 
    before going into the task_loss. Default is nn.Identity().

    The kd_loss_fn takes args (zs, zt, qs, qt, y) where zs and zt are the 
    student and teacher embeddings, qs and qt are the student and teacher
    head outputs, and y is the targets for the dataset. Default is 0.5 * F.mse_loss(zs, zt).

    The loss function used during training is task_loss + kd_loss.
    '''
    def __init__(
            self, 
            teacher_encoder,
            student_encoder,
            task_loss_fn,
            teacher_head=nn.Identity(),
            student_head=nn.Identity(),
            kd_loss_fn=lambda zs, zt, qs, qt, y: 0.5 * F.mse_loss(zs, zt),
            learning_rate=1e-4,
            weight_decay=0.01,
        ):
        super().__init__()

        self.teacher_encoder = teacher_encoder
        self.student_encoder = student_encoder

        self.teacher_head = teacher_head
        self.student_head = student_head

        for param in self.teacher_encoder.parameters():
            param.requires_grad = False

        for param in self.teacher_head.parameters():
            param.requires_grad = False

        self.task_loss_fn = task_loss_fn
        self.kd_loss_fn = kd_loss_fn
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
       
        # freeze the teacher model
        self.teacher_encoder.eval()
        self.teacher_head.eval()

        self.save_hyperparameters(ignore=['teacher_encoder', 'teacher_head', 'student_encoder', 'student_head'])

    def training_step(self, batch, batch_idx):
        x, y = batch
        zt = self.teacher_encoder(x)
        qt = self.teacher_head(zt)

        zs = self.student_encoder(x)
        qs = self.student_head(zs)
        
        task_loss = self.task_loss_fn(zs, zt, qs, qt, y)
        kd_loss = self.kd_loss_fn(zs, zt, qs, qt, y)

        self.log('task_loss', task_loss, prog_bar=True)
        self.log('kd_loss', kd_loss, prog_bar=True)

        loss = task_loss + kd_loss
        self.log('train_loss', loss, prog_bar=True)

        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        zt = self.teacher_encoder(x)
        qt = self.teacher_head(zt)

        zs = self.student_encoder(x)
        qs = self.student_head(zs)

        task_loss = self.task_loss_fn(zs, zt, qs, qt, y)
        kd_loss = self.kd_loss_fn(zs, zt, qs, qt, y)
        self.log('val_task_loss', task_loss, prog_bar=True)
        self.log('val_kd_loss', kd_loss, prog_bar=True)

        loss = task_loss + kd_loss
        self.log('val_loss', loss, prog_bar=True)

        return loss

    def configure_optimizers(self):
        optimizer = optim.AdamW(self.parameters(), lr=self.learning_rate, weight_decay=self.weight_decay)
        # scheduler = optim.lr_scheduler.SequentialLR(optimizer, schedulers=[
        #     optim.lr_scheduler.LinearLR(optimizer, 0.33, 1.0, total_iters=5),
        #     optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3, factor=0.5),
        # ],
        # milestones=[1])
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3, factor=0.5)
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                "monitor": "val_task_loss",
            }
        }


