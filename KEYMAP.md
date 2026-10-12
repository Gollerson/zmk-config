Eyelash Sofle — Keymap Übersicht
==============================================================================

Zeilen: Nummern / QWERT / ASDF / ZXCV / Daumen
Spalten: LINKE HAND (6) | JOY | RECHTE HAND (6)
|JOY| = 5-Wege-Joystick (BASE: Pfeile, Press = Enter)
L1=SYM  L2=NAV  L3=SYS  (Daumen-Hold)

+----------------------------------------------------------------------------+
| BASE                                                                      |
+----------------------------------------------------------------------------+
  Esc    1     2     3     4     5   |Up |   6     7     8     9     0     ?  
  Tab    Q     W     E     R     T   |Dn |   Y     U     I     O     P     \  
 Caps    A     S     D     F     G   |Lt |   H     J     K     L     ;     '  
 LShft   Z     X     C     V     B   |Rt |   N     M     ,     .     /     -  
 --------------------------------------------------------------------------
 Mute  LCtrl LGui  LAlt  Space  L1   |Enter| Enter  Bspc   L2    L3   RShft

+----------------------------------------------------------------------------+
| SYM — every symbol as one keypress (no Shift), F1-F12                     |
+----------------------------------------------------------------------------+
   F1    F2    F3    F4    F5    F6   |Up |  F7    F8    F9    F10   F11   F12 
   !     @     #     $     %     ^    |Dn |   &     *     :     "     <     >  
   `     ~     =     +     _     |    |Lt |   (     )     [     ]     {     }  
   -     /     \     ;     '     ,    |Rt |   .     ?     .     .     .     .  
 --------------------------------------------------------------------------
   .     .     .     .     .     .   | . |   .     .     .     .     .  

+----------------------------------------------------------------------------+
| NAV — vim text objects / motions / search / jump list / VS Code           |
+----------------------------------------------------------------------------+
  ci"   ci'   ci(   ci[   ci{   va{  |Up |   *    PgUp  Home   Up    End  PgDn 
  Esc    .     .     .     .     .   |Dn |   [m    ]m    [[    ]]    {     }  
 LCtrl  ciw   "+y   "+p   "_d    .   |Lt |   #     %    :%s/   =     >>    <<  
 LShft  C-o   C-i   g;    g,     .   |Rt | Ctrl+/ Ctrl+F Ctrl+S Ctrl+B C-S-P Del 
 --------------------------------------------------------------------------
   .     .     .     .     .     .   | . |   .     .     .     .     .  

+----------------------------------------------------------------------------+
| SYS — bluetooth / output / media / brightness / screenshot / rgb           |
+----------------------------------------------------------------------------+
   .    BT1   BT2   BT3   BT4   BT5  |Up | BTclr BTall Bri+  Bri-  Mute    .  
   .   OutUSB OutBLE  .     .     .   |Dn | Vol+  Vol-  Prev  Play  Next    .  
   .   Reset Boot    .     .     .   |Lt | PrtSc Lock   .     .     .      .  
   .   SOff RGBOff RGBOn RGBEff RGBBri|Rt |   .     .     .     .   RGBBrd   .  
 --------------------------------------------------------------------------
   .     .     .     .     .     .   | . |   .     .     .     .     .  

==============================================================================
Notes
  - SYM: all 32 US symbols are single keys. Symbols unreachable on BASE
    ( ` ~ = + [ ] { } ) sit on the home row; Shift+base symbols on the top
    row; symbols already direct on BASE ( - / \ ; ' , . ? ) on the bottom.
  - NAV: F-keys moved to SYM, so the top-left row is a text-object cluster.
    Joystick = arrows. [ ] { } etc. are macros so no SYM hop is needed.
  - SYS: F6-F12 removed; the right hand is media / brightness / screenshot
    (PrtSc) / screen lock instead.
