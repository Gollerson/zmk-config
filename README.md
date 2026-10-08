# zmk-config — PandaKB Eyelash Sofle

ZMK firmware config for a **PandaKB Eyelash Sofle** split keyboard running two
**nice!nano v2** controllers. Coding-optimized layout.

## Hardware

| | |
|---|---|
| Controllers | 2 × nice!nano v2 (nRF52840) |
| Shield | `eyelash_sofle_left` / `eyelash_sofle_right` |
| Displays | nice!view (optional; remove `nice_view` from `build.yaml` if not fitted) |
| Left side | EC11 rotary encoder (ZMK sensor) |
| Right side | 5-way joystick (up/down/left/right/press) |
| Thumb keys | 5 per side |

The joystick is **not** a ZMK sensor — it is wired as matrix keys in the
inner column (`RC(x,7)`):

| Joystick | Matrix index |
|----------|--------------|
| UP       | 6            |
| DOWN     | 19           |
| LEFT     | 32           |
| RIGHT    | 45           |
| PRESS    | 58           |

Left encoder press is matrix index 52.

## Layout

5 layers:

| # | Name | Summary |
|---|------|---------|
| 0 | BASE | QWERTY, mods on thumbs, left encoder = volume |
| 1 | SYM | Code symbols; mod-morph brackets (`(`/`)`, `[`/`]`, `{`/`}`, `<`/`>`, `'`/`"`) |
| 2 | NAV | Vim-style nav + vim register macros |
| 3 | NUMFN | Number row / F-keys |
| 4 | SYS | Bluetooth, output, RGB, reset, bootloader, soft off |

### Thumb row

| | Left (outer → inner) | Right (inner → outer) |
|---|---|---|
| | LCtrl, LGui, LAlt, Space, **L1 (SYM)** | **L2 (NAV)**, Enter, Bkspc, **L3 (NUMFN)**, **L4 (SYS)**, RShift |

Left encoder press = Mute.

Layers are reached by **holding** the thumb layer keys on the base layer:
```
L1 → SYM     L2 → NAV     L3 → NUMFN     L4 → SYS
```
On each layer the layer keys are transparent, so holds keep working while you
move between layers.

### Symbols (Layer 1)

Tap mod-morphs, or Shift+tap to get the closing bracket:

| Key | Tap | Shift+Tap |
|-----|-----|-----------|
| `paren` | `(` | `)` |
| `brack` | `[` | `]` |
| `brace` | `{` | `}` |
| `angle` | `<` | `>` |
| `quote` | `'` | `"` |

### Vim macros (Layer 2, left hand home row)

| Key | Sends |
|-----|-------|
| `vim_gg` | `gg` |
| `vim_ciw` | `ciw` |
| `vim_yank` | `"+y` |
| `vim_paste` | `"+p` |
| `vim_dd` | `dd` |
| `vim_yy` | `yy` (on the physical Y key) |

> Macros emit HID usages, so they follow the **host OS layout**. On a US host
> layout these produce exactly `"+y` / `"+p`. Set your OS to US (or a US-based
> variant) for the intended behavior.

## Debugging the matrix

`config/debug_eyelash_sofle.keymap` is a helper that types each matrix position's
index (e.g. `052`) so you can identify which physical key maps to which index.
To use it, temporarily replace `config/eyelash_sofle.keymap` with it and build.

## Building

Firmware builds in GitHub Actions via `.github/workflows/build.yml`
(`zmkfirmware/zmk` reusable workflow). Push to this repo and download the
artifacts, or run the workflow manually via **Actions → Run workflow**.

## Flashing

1. Put a half into bootloader mode: **double-tap reset** (or press reset once).
2. It mounts as a USB drive named `NICENANO`.
3. Drag the matching `.uf2` onto it:
   - `eyelash_sofle_left-nice_nano_v2-*.uf2` → left half
   - `eyelash_sofle_right-nice_nano_v2-*.uf2` → right half
   - `settings_reset-nice_nano_v2-*.uf2` → clears settings (use if the halves
     won't pair; flash to **both** halves, then re-flash the real firmware)
4. It reboots automatically. The left half is the central/connected side.

## Editing the layout

- **By hand:** edit `config/eyelash_sofle.keymap`.
- **Graphically:** the left build enables ZMK Studio
  (`-DCONFIG_ZMK_STUDIO=y`), so you can connect the left half over USB and
  remap live at <https://zmk.studio>.

## Rebuilding from scratch

`west.yml` pulls the `eyelash_sofle` shield from
<https://github.com/a741725193/zmk-sofle> and pins ZMK to `v0.3.0`.
