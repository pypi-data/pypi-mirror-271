from __future__ import annotations

import pytest
from yarl import URL

from instawow.definitions import Defn
from instawow.manager_ctx import ManagerCtx
from instawow.pkg_management import PkgManager
from instawow.pkg_models import Pkg
from instawow_wa_updater._core import WaCompanionBuilder, WeakAura, WeakAuras


@pytest.fixture
def _wa_saved_vars(
    iw_manager_ctx: ManagerCtx,
):
    saved_vars = (
        iw_manager_ctx.config.addon_dir.parents[1] / 'WTF' / 'Account' / 'test' / 'SavedVariables'
    )
    saved_vars.mkdir(parents=True)
    (saved_vars / WeakAuras.addon_name).with_suffix('.lua').write_text(
        """\
WeakAurasSaved = {
    ["displays"] = {
        ["Foo"] = {
            ["bar"] = "baz",
        },
    },
}
"""
    )


@pytest.fixture
def builder(
    iw_manager_ctx: ManagerCtx,
):
    return WaCompanionBuilder(iw_manager_ctx)


def test_can_parse_empty_displays_table(
    builder: WaCompanionBuilder,
):
    assert (
        builder.extract_auras(
            WeakAuras,
            """\
WeakAurasSaved = {
    ["displays"] = {
    },
}
""",
        ).root
        == {}
    )


def test_urlless_display_is_discarded(
    builder: WaCompanionBuilder,
):
    assert (
        builder.extract_auras(
            WeakAuras,
            """\
WeakAurasSaved = {
    ["displays"] = {
        ["Foo"] = {
            ["bar"] = "baz",
        },
    },
}
""",
        ).root
        == {}
    )


def test_can_parse_minimal_wago_display(
    builder: WaCompanionBuilder,
):
    aura = WeakAura(
        id='foo',
        uid='foo',
        parent=None,
        url=URL('https://wago.io/foo/1'),
        version=1,
    )
    assert builder.extract_auras(
        WeakAuras,
        """\
WeakAurasSaved = {
    ["displays"] = {
        ["Foo"] = {
            ["bar"] = "baz",
            ["url"] = "https://wago.io/foo/1",
            ["version"] = 1,
            ["id"] = "foo",
            ["uid"] = "foo",
        },
    },
}
""",
    ).root == {'foo': [aura]}


def test_url_host_not_wago_display_is_discarded(
    builder: WaCompanionBuilder,
):
    assert (
        builder.extract_auras(
            WeakAuras,
            """\
WeakAurasSaved = {
    ["displays"] = {
        ["Foo"] = {
            ["bar"] = "baz",
            ["url"] = "https://wafo.io/foo/1",
            ["version"] = 1,
            ["id"] = "foo",
            ["uid"] = "foo",
        },
    },
}
""",
        ).root
        == {}
    )


def test_can_build_addon_with_empty_seq(
    builder: WaCompanionBuilder,
):
    builder._generate_addon([])


@pytest.mark.usefixtures('_wa_saved_vars')
async def test_can_build_addon_with_mock_saved_vars(
    builder: WaCompanionBuilder,
):
    await builder.build()


def test_build_is_reproducible(
    builder: WaCompanionBuilder,
):
    builder._generate_addon([])
    checksum = builder.get_version()
    builder._generate_addon([])
    assert checksum == builder.get_version()


def test_changelog_is_generated(
    builder: WaCompanionBuilder,
):
    builder._generate_addon([])
    assert builder.changelog_path.read_text() == 'n/a'


async def test_can_resolve_wa_companion_pkg(
    builder: WaCompanionBuilder,
    iw_manager: PkgManager,
):
    await builder.build()
    defn = Defn('instawow', 'weakauras-companion')
    resolve_results = await iw_manager.resolve([defn])
    assert type(resolve_results[defn]) is Pkg


async def test_can_resolve_wa_companion_autoupdate_pkg(
    iw_manager: PkgManager,
):
    defn = Defn('instawow', 'weakauras-companion-autoupdate')
    resolve_results = await iw_manager.resolve([defn])
    assert type(resolve_results[defn]) is Pkg
