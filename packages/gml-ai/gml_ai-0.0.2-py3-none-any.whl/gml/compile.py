from torch.fx.experimental.proxy_tensor import make_fx

#from torch_mlir.torchscript import compile as torch_mlir_compile
from torch_mlir import compile as torch_mlir_compile
from torch_mlir import OutputType
from torch_mlir.dynamo import _get_decomposition_table


def to_torch_mlir(model, example_inputs):
    # Running the model a few times on the inputs, leads to more consistent compiled results.
    # TODO(james): would be good to understand why this is the case.
    for _ in range(2):
        _ = model(*example_inputs)

    model = make_fx(model, pre_dispatch=True, decomposition_table=_get_decomposition_table())(*example_inputs)

    compiled = torch_mlir_compile(
        model,
        example_inputs,
        use_tracing=False,
        ignore_traced_shapes=False,
        output_type=OutputType.RAW,
        use_make_fx=False,
    )

    return compiled
