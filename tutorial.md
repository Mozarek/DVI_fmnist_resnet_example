# Start

pip install -r dvi/requirements
git clone fmnistresnet # TODO
pip install pytorch-lightning
pip install setuptools==59.5.0

Change module.py line 3 from:
`from pytorch_lightning.metrics import Accuracy`
to:
`from torchmetrics import Accuracy`

In module.py remove following import:
`from pytorch_lightning.core.decorators import auto_move_data`

In train.py change:
```py
    checkpoint = ModelCheckpoint(
        filepath=os.path.join(args.filepath, args.classifier, "{epoch:03d}"),
        monitor="acc/val",
        mode="max",
        # save_last=False,
        period=args.period,
        save_top_k=args.save_top_k,
        save_weights_only=True,
    )
```
to:
```py
    checkpoint = ModelCheckpoint(
        filepath=os.path.join(args.filepath, args.classifier, "{epoch:03d}"),
        monitor="acc/val",
        # mode="max",
        # save_last=False,
        period=args.period,
        save_top_k=args.save_top_k,
        save_weights_only=True,
    )
```

In module.py change occurence of:
`self.hparams = hparams`
to:
`self.save_hyperparameters(hparams)`

In data.py change:
`self.hparams = args`
to:
`self.save_hyperparameters(args)`

In data.py line 59 change:
`os.mkdir` to `os.makedirs`

In module.py line 76 change:
`total_steps = self.hparams.max_epochs * len(self.dataloader())`
to:
`total_steps = self.hparams.max_epochs * len(self.trainer._data_connector._train_dataloader_source.dataloader())`

Protobuf 3.19.4 to 3.9.2