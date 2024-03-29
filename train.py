"""
https://github.com/marrrcin/pytorch-resnet-mnist/blob/master/pytorch-resnet-mnist.ipynb
https://github.com/huyvnphan/PyTorch_CIFAR10/tree/master/cifar10_models
"""
import os
from argparse import ArgumentParser

import torch
from pytorch_lightning import Trainer, seed_everything
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger, TensorBoardLogger

from data import FashionMNISTData
from module import FashionMNISTModule


def main(args):

    seed_everything(0)
    # os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_id

    if args.logger == "wandb":
        logger = WandbLogger(name=args.classifier, project="mnist")
    elif args.logger == "tensorboard":
        logger = TensorBoardLogger("mnist", name=args.classifier)

    checkpoint = ModelCheckpoint(
        dirpath=os.path.join(args.filepath, args.classifier),
        filename="{epoch:03d}",
        monitor="acc/val",
        # mode="max",
        # save_last=False,
        every_n_epochs=args.period,
        save_top_k=args.save_top_k,
        save_weights_only=True,
    )

    trainer = Trainer(
        fast_dev_run=bool(args.dev),
        logger=logger if not bool(args.dev + args.test_phase) else None,
        gpus=args.gpus,
        deterministic=True,
        weights_summary=None,
        log_every_n_steps=1,
        max_epochs=args.max_epochs,
        callbacks=checkpoint,
        precision=args.precision,
        enable_progress_bar=True,
    )

    model = FashionMNISTModule(args)
    data = FashionMNISTData(args)
    trainloader = data.train_dataloader()
    data.save_train_data(trainloader, args.filepath)
    testloader = data.test_dataloader()
    data.save_test_data(testloader, args.filepath)


    # if bool(args.pretrained):
    #     state_dict = os.path.join(
    #         "cifar10_models", "state_dicts", args.classifier + ".pt"
    #     )
    #     model.model.load_state_dict(torch.load(state_dict))

    if bool(args.test_phase):
        trainer.test(model, data.test_dataloader())
    else:
        trainer.fit(model, data)
        trainer.test(model, data.test_dataloader())


if __name__ == "__main__":
    parser = ArgumentParser()

    # PROGRAM level args
    parser.add_argument("--data_dir", type=str, default="data")
    # parser.add_argument("--download_weights", type=int, default=0, choices=[0, 1])
    parser.add_argument("--test_phase", type=int, default=0, choices=[0, 1])
    parser.add_argument("--dev", type=int, default=0, choices=[0, 1])
    parser.add_argument(
        "--logger", type=str, default="tensorboard", choices=["tensorboard", "wandb"]
    )

    # TRAINER args
    parser.add_argument("--classifier", type=str, default="mobilenet_v2")
    # parser.add_argument("--pretrained", type=int, default=0, choices=[0, 1])

    parser.add_argument("--precision", type=int, default=32, choices=[16, 32])
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--max_epochs", type=int, default=50)
    parser.add_argument("--num_workers", type=int, default=2)
    parser.add_argument("--gpus", type=str, default="0")

    parser.add_argument("--learning_rate", type=float, default=5e-3)
    parser.add_argument("--weight_decay", type=float, default=1e-2)

    parser.add_argument("--filepath", type=str, default="models")
    parser.add_argument("--period", type=int, default=1)
    parser.add_argument("--save_top_k", type=int, default=-1)

    args = parser.parse_args()
    main(args)
