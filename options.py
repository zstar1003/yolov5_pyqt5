import argparse

class TestOptions():
  def __init__(self):
    self.parser = argparse.ArgumentParser()
    # data loader related
    self.parser.add_argument('--dataroot', type=str, default='./datasets', help='path of data')
    self.parser.add_argument('--dataname', type=str, default='', help='name of dataset')
    self.parser.add_argument('--phase', type=str, default='test', help='phase for dataloading')
    self.parser.add_argument('--batch_size', type=int, default=1, help='batch size')
    self.parser.add_argument('--nThreads', type=int, default=0, help='# of threads for data loader')
    ## mode related
    self.parser.add_argument('--class_nb', type=int, default=9, help='class number for segmentation model')
    self.parser.add_argument('--resume', type=str, default='./results/PSFusion/checkpoints/best_model.pth', help='specified the dir of saved models for resume the training')
    self.parser.add_argument('--gpu', type=int, default=0, help='GPU id')
    # results related
    self.parser.add_argument('--name', type=str, default='PSFusion', help='folder name to save outputs')
    self.parser.add_argument('--result_dir', type=str, default='./Fusion_results', help='path for saving result images and models')
    
  def parse(self):
    self.opt = self.parser.parse_args()
    args = vars(self.opt)
    print('\n--- load options ---')
    for name, value in sorted(args.items()):
      print('%s: %s' % (str(name), str(value)))
    return self.opt
