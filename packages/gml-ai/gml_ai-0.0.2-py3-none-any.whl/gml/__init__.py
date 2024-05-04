from gml.compile import to_torch_mlir


def upload(model, example_inputs):
    compiled = to_torch_mlir(model, example_inputs)

    with open('out.torch.mlir', 'w') as f:
        f.write(str(compiled))
