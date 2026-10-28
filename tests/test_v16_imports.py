import importlib


def test_login_hook_imports():
	importlib.import_module("rada.login_log_hooks")


def test_engine_override_extends_original_controller():
	from rada.engine.engine import Engine
	from rada.rada.doctype.engine.engine import Engine as OriginalEngine

	assert issubclass(Engine, OriginalEngine)
