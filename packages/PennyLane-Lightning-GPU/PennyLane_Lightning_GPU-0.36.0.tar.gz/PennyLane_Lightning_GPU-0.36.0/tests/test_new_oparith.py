
import numpy as np
import pennylane as qml
import pytest



class TestOpMathBench:
    "Test PennyLane new arithmetic operators"

    def test_prod_enable(self, benchmark):

        qml.operation.enable_new_opmath()

        def workflow():

            @qml.qnode(qml.device('lightning.qubit', wires=3))
            def circuit(x: float, y: float):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)
                qml.RX(x + y, wires=2)
                qml.CNOT(wires=[0, 1])
                return qml.expval(qml.PauliX(wires=0) @ qml.PauliZ(wires=1) @ qml.Identity(wires=2))
                # return qml.expval(
                #     qml.ops.op_math.Prod(
                #         qml.PauliX(wires=0), qml.PauliZ(wires=1), qml.Identity(wires=2)
                #     )
                # )

            return circuit

        result_enb = benchmark(workflow)(np.pi / 4, np.pi / 2)
        assert np.allclose(np.array(-0.70710678), result_enb)

    def test_prod_disable(self, benchmark):

        qml.operation.disable_new_opmath()

        def workflow():

            @qml.qnode(qml.device('lightning.qubit', wires=3))
            def circuit(x: float, y: float):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)
                qml.RX(x + y, wires=2)
                qml.CNOT(wires=[0, 1])
                return qml.expval(qml.PauliX(wires=0) @ qml.PauliZ(wires=1) @ qml.Identity(wires=2))
                # return qml.expval(
                #     qml.ops.op_math.Prod(
                #         qml.PauliX(wires=0), qml.PauliZ(wires=1), qml.Identity(wires=2)
                #     )
                # )

            return circuit

        result_dis = benchmark(workflow)(np.pi / 4, np.pi / 2)
        assert np.allclose(np.array(-0.70710678), result_dis)

    def test_sum_enable(self, benchmark):

        qml.operation.enable_new_opmath()

        def workflow():

            @qml.qnode(qml.device('lightning.qubit', wires=3))
            def circuit(x: float, y: float):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)
                qml.RX(x + y, wires=2)
                qml.CNOT(wires=[0, 1])
                return qml.expval(qml.PauliX(wires=0) + qml.PauliY(wires=1) + qml.PauliZ(wires=2))

            return circuit

        result_enb = benchmark(workflow)(np.pi / 4, np.pi / 2)

        assert np.allclose(np.array(-1.41421356), result_enb)

    def test_sum_disable(self, benchmark):

        qml.operation.disable_new_opmath()

        def workflow():

            @qml.qnode(qml.device('lightning.qubit', wires=3))
            def circuit(x: float, y: float):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)
                qml.RX(x + y, wires=2)
                qml.CNOT(wires=[0, 1])
                return qml.expval(qml.PauliX(wires=0) + qml.PauliY(wires=1) + qml.PauliZ(wires=2))

            return circuit

        result_dis = benchmark(workflow)(np.pi / 4, np.pi / 2)

        assert np.allclose(np.array(-1.41421356), result_dis)

    def test_sum_sprod_enable(self, benchmark):

        qml.operation.enable_new_opmath()


        def workflow():
            @qml.qnode(qml.device('lightning.qubit', wires=3))
            def circuit(x: float, y: float):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)
                qml.RX(x + y, wires=2)
                qml.CNOT(wires=[0, 1])
                return qml.expval(0.2 * qml.PauliX(wires=0) + 0.3 * qml.PauliY(wires=1) + 0.5 * qml.PauliZ(wires=2))
            return circuit
        

        result_enb = benchmark(workflow)(np.pi / 4, np.pi / 2)
        assert np.allclose(-0.5656854249492379, result_enb)

    def test_sum_sprod_disable(self, benchmark):

        qml.operation.disable_new_opmath()


        def workflow():
            @qml.qnode(qml.device('lightning.qubit', wires=3))
            def circuit(x: float, y: float):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)
                qml.RX(x + y, wires=2)
                qml.CNOT(wires=[0, 1])
                return qml.expval(0.2 * qml.PauliX(wires=0) + 0.3 * qml.PauliY(wires=1) + 0.5 * qml.PauliZ(wires=2))
            return circuit
        

        result_dis = benchmark(workflow)(np.pi / 4, np.pi / 2)
        assert np.allclose(-0.5656854249492379, result_dis)


    def test_mix_dunder_enable(self, benchmark):

        qml.operation.enable_new_opmath()

        def workflow():

            @qml.qnode(qml.device('lightning.qubit', wires=6))
            def circuit(x, y):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)
                qml.CNOT(wires=[0, 1])
                return qml.expval(-0.5 * qml.PauliX(0) @ qml.PauliY(1) + -0.2 * qml.PauliX(2) @ qml.PauliY(4) + -0.3 * qml.PauliZ(3))

            return circuit
        
        result_enb = benchmark(workflow)(np.pi / 4, np.pi / 4)
        assert np.allclose(-0.0499999, result_enb)

    def test_mix_dunder_disable(self, benchmark):

        qml.operation.disable_new_opmath()

        def workflow():

            @qml.qnode(qml.device('lightning.qubit', wires=6))
            def circuit(x, y):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)
                qml.CNOT(wires=[0, 1])
                return qml.expval(-0.5 * qml.PauliX(0) @ qml.PauliY(1) + -0.2 * qml.PauliX(2) @ qml.PauliY(4) + -0.3 * qml.PauliZ(3))

            return circuit

        result_dis = benchmark(workflow)(np.pi / 4, np.pi / 4)
        assert np.allclose(-0.0499999, result_dis)

    def test_nested_1_enable(self, benchmark):

        qml.operation.enable_new_opmath()

        def workflow():
            @qml.qnode(qml.device('lightning.qubit', wires=4))
            def circuit(x, y):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)

                qml.RX(x + y, wires=2)
                qml.RX(y - x, wires=3)

                qml.CNOT(wires=[0, 1])
                qml.CNOT(wires=[0, 2])

                A = np.array(
                    [[complex(1.0, 0.0), complex(2.0, 0.0)], [complex(2.0, 0.0), complex(1.0, 0.0)]]
                )
                return qml.expval(
                    0.2 * (qml.Hermitian(A, wires=1) + qml.PauliZ(0))
                    + 0.4 * (qml.PauliX(2) @ qml.PauliZ(3))
                )
            return circuit
        
        result_enb = benchmark(workflow)(np.pi / 4, np.pi / 2)
        assert np.allclose(0.34142136, result_enb)

    def test_nested_1_disable(self, benchmark):

        qml.operation.disable_new_opmath()

        def workflow():
            @qml.qnode(qml.device('lightning.qubit', wires=4))
            def circuit(x, y):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)

                qml.RX(x + y, wires=2)
                qml.RX(y - x, wires=3)

                qml.CNOT(wires=[0, 1])
                qml.CNOT(wires=[0, 2])

                A = np.array(
                    [[complex(1.0, 0.0), complex(2.0, 0.0)], [complex(2.0, 0.0), complex(1.0, 0.0)]]
                )
                return qml.expval(
                    0.2 * (qml.Hermitian(A, wires=1) + qml.PauliZ(0))
                    + 0.4 * (qml.PauliX(2) @ qml.PauliZ(3))
                )
            return circuit
        
        result_dis = benchmark(workflow)(np.pi / 4, np.pi / 2)
        assert np.allclose(0.34142136, result_dis)

    def test_nested_2_enable(self, benchmark):

        qml.operation.enable_new_opmath()

        def workflow():
            @qml.qnode(qml.device('lightning.qubit', wires=4))
            def circuit(x, y):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)

                qml.RX(x + y, wires=2)
                qml.RX(y - x, wires=3)

                qml.CNOT(wires=[0, 1])
                qml.CNOT(wires=[0, 2])

                A = np.array(
                    [[complex(1.0, 0.0), complex(2.0, 0.0)], [complex(2.0, 0.0), complex(1.0, 0.0)]]
                )
                return qml.var(
                    (qml.Hermitian(A, wires=1) + qml.PauliZ(0))
                    @ (0.5 * (qml.PauliX(2) @ qml.PauliZ(3)))
                )
            return circuit
        
        result_enb = benchmark(workflow)(np.pi, np.pi)
        assert np.allclose(1.0, result_enb)

    def test_nested_2_disable(self, benchmark):

        qml.operation.disable_new_opmath()

        def workflow():
            @qml.qnode(qml.device('lightning.qubit', wires=4))
            def circuit(x, y):
                qml.RX(x, wires=0)
                qml.RX(y, wires=1)

                qml.RX(x + y, wires=2)
                qml.RX(y - x, wires=3)

                qml.CNOT(wires=[0, 1])
                qml.CNOT(wires=[0, 2])

                A = np.array(
                    [[complex(1.0, 0.0), complex(2.0, 0.0)], [complex(2.0, 0.0), complex(1.0, 0.0)]]
                )
                return qml.var(
                    (qml.Hermitian(A, wires=1) + qml.PauliZ(0))
                    @ (0.5 * (qml.PauliX(2) @ qml.PauliZ(3)))
                )
            return circuit
        
        result_dis = benchmark(workflow)(np.pi, np.pi)
        assert np.allclose(1.0, result_dis)

if __name__ == "__main__":
    pytest.main(["-x", __file__])
