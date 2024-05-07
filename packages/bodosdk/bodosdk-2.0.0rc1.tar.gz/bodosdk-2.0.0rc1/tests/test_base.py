from unittest.mock import patch, call

import pytest

from bodosdk.base import SDKBaseModel
from bodosdk.deprecation_decorator import check_deprecation


class TestSDKBaseModel:
    def setup_method(self):
        self.deprecated_fields = {
            "test_field": {
                "version": "1.2",
                "end_of_support": "2023-12-31",
                "notes": "Use anotherField instead",
            },
            "test_field2": {
                "version": "1.2",
                "end_of_support": "2023-12-31",
                "notes": "Use another value instead",
                "deprecated_values": ["test", "test2"],
            },
        }
        self.deprecated_methods = {
            "test_method": {
                "version": "1.2",
                "end_of_support": "2023-12-31",
                "notes": "Use anotherMethod instead",
            }
        }

    def test_initialization_kwargs(self):
        model = SDKBaseModel(
            _deprecated_fields=self.deprecated_fields,
            _deprecated_methods=self.deprecated_methods,
        )
        assert model._deprecated_fields == self.deprecated_fields
        assert model._deprecated_methods == self.deprecated_methods
        assert model._mutable is False

    def test_initialization_dict(self):
        model = SDKBaseModel(
            **{
                "_deprecated_fields": self.deprecated_fields,
                "_deprecated_methods": self.deprecated_methods,
            }
        )
        assert model._deprecated_fields == self.deprecated_fields
        assert model._deprecated_methods == self.deprecated_methods
        assert model._mutable is False

    def test_initialization_camel_case_dict(self):
        model = SDKBaseModel(
            **{
                "_deprecatedFields": self.deprecated_fields,
                "_deprecatedMethods": self.deprecated_methods,
            }
        )
        assert model._deprecated_fields == self.deprecated_fields
        assert model._deprecated_methods == self.deprecated_methods
        assert model._mutable is False

    def test_camel_case_access(self):
        model = SDKBaseModel(
            **{
                "_deprecatedFields": self.deprecated_fields,
                "_deprecatedMethods": self.deprecated_methods,
            }
        )
        assert model["_deprecatedFields"] == self.deprecated_fields

    def test_immutable_after_initialization(self):
        class TestModel(SDKBaseModel):
            someField: str

        model = TestModel(someField="value")
        with pytest.raises(TypeError, match="Object is immutable"):
            model["someField"] = "newValue"

    def test__update_method(self):
        class TestModel(SDKBaseModel):
            some_dict: dict
            some_int: int

        model = TestModel(some_dict={}, some_int=2)
        model._update({"someDict": {1: "test"}, "someInt": 1})
        assert model.some_dict[1] == "test"
        assert model.some_int == 1

    def test_deprecation_warning(self):
        class TestModel(SDKBaseModel):
            test_field: int
            test_field2: str

            @check_deprecation
            def test_method(self):
                pass

        with patch("bodosdk.base.logging") as log:  # type: Mock
            model = TestModel(
                test_field=1,
                test_field2="test",
                _deprecated_fields=self.deprecated_fields,
                _deprecated_methods=self.deprecated_methods,
            )

            assert model.test_field == 1
            assert model.test_field2 == "test"
            log.warning.assert_has_calls(
                [
                    call(
                        "Field test_field of class TestModel will be deprecated in version 1.2. "
                        "Field will be supported till 2023-12-31. Additional notes: Use anotherField instead"
                    ),
                    call(
                        "Value test for field test_field2 of class TestModel will be deprecated in version 1.2. "
                        "Value be supported till 2023-12-31. Additional notes: Use another value instead"
                    ),
                ]
            )
        with patch("bodosdk.deprecation_decorator.logging") as log:
            model.test_method()
            log.warning.assert_has_calls(
                [
                    call(
                        "Method test_method of class TestModel will be deprecated in version 1.2. "
                        "Method will be supported till 2023-12-31. Additional notes: Use anotherMethod instead"
                    )
                ]
            )
