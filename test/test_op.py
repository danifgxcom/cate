from collections import OrderedDict
from unittest import TestCase

from ect.core.op import OpRegistry, op, op_input, op_return, op_output
from ect.core.util import object_to_qualified_name


class OpTest(TestCase):
    def setUp(self):
        self.registry = OpRegistry()

    def tearDown(self):
        self.registry = None

    def test_f(self):
        def f(a: float, b, c, u=3, v='A', w=4.9) -> str:
            """Hi, I am f!"""
            return str(a + b + c + u + len(v) + w)

        registry = self.registry
        added_op_reg = registry.add_op(f)
        self.assertIsNotNone(added_op_reg)

        with self.assertRaises(ValueError):
            registry.add_op(f, fail_if_exists=True)

        self.assertIs(registry.add_op(f, fail_if_exists=False), added_op_reg)

        op_reg = registry.get_op(object_to_qualified_name(f))
        self.assertIs(op_reg, added_op_reg)
        self.assertIs(op_reg.operation, f)
        self.assertIsNotNone(op_reg.meta_info)
        self.assertEqual(op_reg.meta_info.qualified_name, object_to_qualified_name(f))
        self.assertEqual(op_reg.meta_info.attributes, dict(description='Hi, I am f!'))
        expected_inputs = OrderedDict()
        expected_inputs['a'] = dict(data_type=float)
        expected_inputs['b'] = dict()
        expected_inputs['c'] = dict()
        expected_inputs['u'] = dict(default_value=3)
        expected_inputs['v'] = dict(default_value='A')
        expected_inputs['w'] = dict(default_value=4.9)
        self.assertEqual(op_reg.meta_info.inputs, expected_inputs)
        expected_outputs = OrderedDict()
        expected_outputs['return'] = dict(data_type=str)
        self.assertEqual(op_reg.meta_info.outputs, expected_outputs)

        removed_op_reg = registry.remove_op(f)
        self.assertIs(removed_op_reg, op_reg)
        op_reg = registry.get_op(object_to_qualified_name(f))
        self.assertIsNone(op_reg)

        with self.assertRaises(ValueError):
            registry.remove_op(f, fail_if_not_exists=True)

    def test_f_op(self):
        @op(registry=self.registry)
        def f_op(a: float, b, c, u=3, v='A', w=4.9) -> str:
            """Hi, I am f_op!"""
            return str(a + b + c + u + len(v) + w)

        with self.assertRaises(ValueError):
            # must exist
            self.registry.add_op(f_op, fail_if_exists=True)

        op_reg = self.registry.get_op(object_to_qualified_name(f_op))
        self.assertIs(op_reg.operation, f_op)
        self.assertIsNotNone(op_reg.meta_info)
        self.assertEqual(op_reg.meta_info.qualified_name, object_to_qualified_name(f_op))
        self.assertEqual(op_reg.meta_info.attributes, dict(description='Hi, I am f_op!'))
        expected_inputs = OrderedDict()
        expected_inputs['a'] = dict(data_type=float)
        expected_inputs['b'] = dict()
        expected_inputs['c'] = dict()
        expected_inputs['u'] = dict(default_value=3)
        expected_inputs['v'] = dict(default_value='A')
        expected_inputs['w'] = dict(default_value=4.9)
        self.assertEqual(op_reg.meta_info.inputs, expected_inputs)
        expected_outputs = OrderedDict()
        expected_outputs['return'] = dict(data_type=str)
        self.assertEqual(op_reg.meta_info.outputs, expected_outputs)

    def test_f_op_inp_ret(self):
        @op_input('a', value_range=[0., 1.], registry=self.registry)
        @op_input('v', value_set=['A', 'B', 'C'], registry=self.registry)
        @op_return(not_none=True, registry=self.registry)
        def f_op_inp_ret(a: float, b, c, u=3, v='A', w=4.9) -> str:
            """Hi, I am f_op_inp_ret!"""
            return str(a + b + c + u + len(v) + w)

        with self.assertRaises(ValueError):
            # must exist
            self.registry.add_op(f_op_inp_ret, fail_if_exists=True)

        op_reg = self.registry.get_op(object_to_qualified_name(f_op_inp_ret))
        self.assertIs(op_reg.operation, f_op_inp_ret)
        self.assertIsNotNone(op_reg.meta_info)
        self.assertEqual(op_reg.meta_info.qualified_name, object_to_qualified_name(f_op_inp_ret))
        self.assertEqual(op_reg.meta_info.attributes, dict(description='Hi, I am f_op_inp_ret!'))
        expected_inputs = OrderedDict()
        expected_inputs['a'] = dict(data_type=float, value_range=[0., 1.])
        expected_inputs['b'] = dict()
        expected_inputs['c'] = dict()
        expected_inputs['u'] = dict(default_value=3)
        expected_inputs['v'] = dict(default_value='A', value_set=['A', 'B', 'C'])
        expected_inputs['w'] = dict(default_value=4.9)
        self.assertEqual(op_reg.meta_info.inputs, expected_inputs)
        expected_outputs = OrderedDict()
        expected_outputs['return'] = dict(data_type=str, not_none=True)
        self.assertEqual(op_reg.meta_info.outputs, expected_outputs)

    def test_C(self):
        class C:
            """Hi, I am C!"""

            def __call__(self):
                return None

        registry = self.registry
        added_op_reg = registry.add_op(C)
        self.assertIsNotNone(added_op_reg)

        with self.assertRaises(ValueError):
            registry.add_op(C, fail_if_exists=True)

        self.assertIs(registry.add_op(C, fail_if_exists=False), added_op_reg)

        op_reg = registry.get_op(object_to_qualified_name(C))
        self.assertIs(op_reg, added_op_reg)
        self.assertIs(op_reg.operation, C)
        self.assertIsNotNone(op_reg.meta_info)
        self.assertEqual(op_reg.meta_info.qualified_name, object_to_qualified_name(C))
        self.assertEqual(op_reg.meta_info.attributes, dict(description='Hi, I am C!'))
        self.assertEqual(op_reg.meta_info.inputs, OrderedDict())
        self.assertEqual(op_reg.meta_info.outputs, OrderedDict())

        removed_op_reg = registry.remove_op(C)
        self.assertIs(removed_op_reg, op_reg)
        op_reg = registry.get_op(object_to_qualified_name(C))
        self.assertIsNone(op_reg)

        with self.assertRaises(ValueError):
            registry.remove_op(C, fail_if_not_exists=True)

    def test_C_op(self):
        @op(registry=self.registry)
        class C_op:
            """Hi, I am C_op!"""

            def __call__(self):
                return None

        with self.assertRaises(ValueError):
            # must exist
            self.registry.add_op(C_op, fail_if_exists=True)

        op_reg = self.registry.get_op(object_to_qualified_name(C_op))
        self.assertIs(op_reg.operation, C_op)
        self.assertIsNotNone(op_reg.meta_info)
        self.assertEqual(op_reg.meta_info.qualified_name, object_to_qualified_name(C_op))
        self.assertEqual(op_reg.meta_info.attributes, dict(description='Hi, I am C_op!'))
        self.assertEqual(op_reg.meta_info.inputs, OrderedDict())
        self.assertEqual(op_reg.meta_info.outputs, OrderedDict())

    def test_C_op_inp_out(self):
        @op_input('a', data_type=float, default_value=0.5, value_range=[0., 1.], registry=self.registry)
        @op_input('b', data_type=str, default_value='A', value_set=['A', 'B', 'C'], registry=self.registry)
        @op_output('x', data_type=float, registry=self.registry)
        @op_output('y', data_type=list, registry=self.registry)
        class C_op_inp_out:
            """Hi, I am C_op_inp_out!"""

            def __init__(self):
                self.a = None
                self.b = None
                self.x = None
                self.y = None

            def __call__(self):
                self.x = 2.5 * self.a
                self.y = [self.a, self.b]

        with self.assertRaises(ValueError):
            # must exist
            self.registry.add_op(C_op_inp_out, fail_if_exists=True)

        op_reg = self.registry.get_op(object_to_qualified_name(C_op_inp_out))
        self.assertIs(op_reg.operation, C_op_inp_out)
        self.assertIsNotNone(op_reg.meta_info)
        self.assertEqual(op_reg.meta_info.qualified_name, object_to_qualified_name(C_op_inp_out))
        self.assertEqual(op_reg.meta_info.attributes, dict(description='Hi, I am C_op_inp_out!'))
        expected_inputs = OrderedDict()
        expected_inputs['b'] = dict(data_type=str, default_value='A', value_set=['A', 'B', 'C'])
        expected_inputs['a'] = dict(data_type=float, default_value=0.5, value_range=[0., 1.])
        self.assertEqual(op_reg.meta_info.inputs, expected_inputs)
        expected_outputs = OrderedDict()
        expected_outputs['y'] = dict(data_type=list)
        expected_outputs['x'] = dict(data_type=float)
        self.assertEqual(op_reg.meta_info.outputs, expected_outputs)

    def test_json_encode_decode(self):

        @op_input('a', data_type=float, default_value=0.5, value_range=[0., 1.], registry=self.registry)
        @op_input('b', data_type=str, default_value='A', value_set=['A', 'B', 'C'], registry=self.registry)
        @op_output('x', data_type=float, registry=self.registry)
        @op_output('y', data_type=list, registry=self.registry)
        class C:
            """I am C!"""
            pass

        import json
        from io import StringIO
        from ect.core.util import object_to_qualified_name

        def convert_connectors_to_json(connector_dict):
            connectors_copy = OrderedDict()
            for connector_name, properties in connector_dict.items():
                properties_copy = dict(properties)
                if 'data_type' in properties_copy:
                    properties_copy['data_type'] = object_to_qualified_name(properties_copy['data_type'])
                connectors_copy[connector_name] = properties_copy
            return connectors_copy

        op_reg = self.registry.get_op(object_to_qualified_name(C))
        meta_info = op_reg.meta_info

        d1 = OrderedDict()
        d1['qualified_name'] = meta_info.qualified_name
        d1['attributes'] = meta_info.attributes
        d1['inputs'] = convert_connectors_to_json(meta_info.inputs)
        d1['outputs'] = convert_connectors_to_json(meta_info.outputs)
        s = json.dumps(d1, indent='  ')
        d2 = json.load(StringIO(s))

        self.assertEqual(d2, d1)