BUILD_DIR=build
SHELLCHECK_VERSION=v0.7.1

.PHONY: test
test: shellcheck zsd bats editorconfigchecker


# Zadanie uruchamiające editorconfig-checkera
.PHONY: editorconfigchecker
editorconfigchecker: install_editorconfigchecker_if_missing
	$(BUILD_DIR)/editorconfigchecker/bin/ec

# Zadanie instalujące editorconfigchecker, jesli nie został już zainstalowany / ściągnięty
.PHONY: install_editorconfigchecker_if_missing
install_editorconfigchecker_if_missing:
	bash -c "(test -f $(BUILD_DIR)/editorconfigchecker/bin/ec || tools/build-helper.sh download-editorconfigchecker)"

# Zadanie generujące dokumentację dla skryptów Bashowych.
.PHONY: zsd
zsd: install_zshelldoc_if_missing
	tools/build-helper.sh generate-zsd

# Zadanie instalujące ZShell Doc, jeśli nie został już zainstalowany / ściągnięty.
.PHONY: install_zshelldoc_if_missing
install_zshelldoc_if_missing:
	bash -c "(which zsd || test -f $(BUILD_DIR)/zsd/bin/zsd && echo 'zsd zainstalowany') || tools/build-helper.sh install-zsd"

# Zadanie uruchamiające Shellcheck.
.PHONY: shellcheck
shellcheck: install_shellcheck_if_missing
	$(eval SHELLCHECK_CMD = $(shell bash -c "which shellcheck || echo '$(BUILD_DIR)/shellcheck-$(SHELLCHECK_VERSION)/shellcheck'"))
	find src -name "*.sh" | grep -v /zsdoc/ | xargs $(SHELLCHECK_CMD)

# Zadanie instalujące Shellcheck jeśli go nie ma.
.PHONY: install_shellcheck_if_missing
install_shellcheck_if_missing:
	bash -c "(which shellcheck || test -f $(BUILD_DIR)/shellcheck-$(SHELLCHECK_VERSION)}/shellcheck && echo 'shellcheck zainstalowany') || tools/build-helper.sh download-shellcheck"

# Zadanie uruchamiające testy Bats.
.PHONY: bats
bats: install_bats_if_missing
	$(eval BATS_CMD = $(shell bash -c "which bats || echo '$(BUILD_DIR)/bats/bin/bats'"))
	$(BATS_CMD) -t src/test/bats

# Zadanie instalujące Bats, jeśli nie został już zainstalowany / ściągnięty.
.PHONY: install_bats_if_missing
install_bats_if_missing: submodules-init
	bash -c "(which bats || test -f $(BUILD_DIR)/bats/bin/bats && echo 'bats zainstalowany') || tools/build-helper.sh download-bats"

# Zadanie inicjujące submoduły gitowe.
.PHONY: submodules-init
submodules-init:
	tools/build-helper.sh initialize-submodules
