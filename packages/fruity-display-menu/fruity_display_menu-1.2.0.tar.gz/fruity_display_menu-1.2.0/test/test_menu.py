import unittest
from unittest.mock import Mock

from adafruit_displayio_sh1106 import SH1106
from displayio import Display, Group

from fruity_menu.abstract import AbstractMenu, AbstractMenuOption
from fruity_menu.adjust import DISPLAY, AdjustMenu
from fruity_menu.options import ActionButton, SubmenuButton, ValueButton
from fruity_menu.menu import Menu, OPT_BACK_COLOR, OPT_HIGHLIGHT_BACK_COLOR, OPT_HIGHLIGHT_TEXT_COLOR, OPT_TEXT_COLOR

HEIGHT = 64
WIDTH = 128
DISPLAY = SH1106

def get_mock_display():
    return Mock(Display(None, [], width=WIDTH, height=HEIGHT))

def TRAP_ACTION():
    raise AssertionError('You should not have executed me!')

def PRINT_ACTION(arg1 = None, arg2 = None, arg3 = None, arg4 = None):
    if (arg1 is not None):
        print('\t',arg1)
    if (arg2 is not None):
        print('\t',arg2)
    if (arg3 is not None):
        print('\t',arg3)
    if (arg4 is not None):
        print('\t',arg4)

def TRUE_ACTION():
    return True

class MenuTests(unittest.TestCase):
    def test_constructor_requiresDisplay(self):
        menu = Menu(get_mock_display(), HEIGHT, WIDTH)

class MenuOptionTests(unittest.TestCase):
    menu = None

    def setUp(self):
        self.menu = Menu(get_mock_display(), WIDTH, HEIGHT)

    def test_menu_constructor_setsFields(self):
        menu_title = 'This is a title'
        menu_show_title = False
        menu = Menu(DISPLAY, HEIGHT, WIDTH, show_menu_title=menu_show_title, title=menu_title)
        self.assertEqual(menu_show_title, menu._show_title)
        self.assertEqual(menu_title, menu._title)


    def test_menu_withoutDisplay_setsFields(self):
        menu_title = 'One more time'
        menu_show_title = True
        h = 16
        w = 16
        menu = Menu.without_display(h, w, menu_show_title, menu_title)
        
        self.assertEqual(menu_title, menu._title)
        self.assertEqual(menu_show_title, menu._show_title)
        self.assertEqual(h, menu._height)
        self.assertEqual(w, menu._width)

    def test_action_constructor_setsFields(self):
        btn_title = 'My title'
        act = ActionButton(btn_title, TRAP_ACTION)
        self.assertEqual(btn_title, act.text, 'Specified button title not set')
        self.assertEqual(TRAP_ACTION, act._action, 'Specified button action not set')

    def test_submenu_constructor_setsFields(self):
        btn_title = 'The subtitler'
        sub = SubmenuButton(btn_title, self.menu, PRINT_ACTION)
        self.assertEqual(btn_title, sub.text, 'Specified title not assigned to button')
        self.assertEqual(self.menu, sub.submenu, 'Specified menu not assigned to button')

    def test_value_constructor(self):
        btn_title = 'valyo'
        btn_val = 890
        val_btn = ValueButton(btn_title, btn_val, Menu(DISPLAY, HEIGHT, WIDTH), PRINT_ACTION)
        self.assertEqual(btn_title, val_btn.text, 'Given title not assigned to button')
        self.assertEqual(btn_val, val_btn.target, 'Given value not assigned to button')

    def test_menuOption_constructor_setsFields(self):
        opt = AbstractMenuOption('My title')
        self.assertEqual(opt.text, 'My title')

    def test_addActionButton_setsFields(self):
        act = self.menu.add_action_button('Perform this', action=TRAP_ACTION)
        self.assertEqual(act.text, 'Perform this', 'Button text does not match string given to method')
        self.assertIn(act, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addSubmenuButton(self):
        somesubmenu = Menu(DISPLAY, HEIGHT, WIDTH, title='Test menu')
        sub = self.menu.add_submenu_button('Title here', sub=somesubmenu)
        self.assertEqual(sub.text, 'Title here', 'Button text does not match string given to method')
        self.assertIn(sub, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addValueButton_int(self):
        someotherval = 123
        val = self.menu.add_value_button('More arg txt', someotherval)
        self.assertEqual(val.text, 'More arg txt', 'Given title not assigned to button')
        self.assertIn(val, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addValueButton_bool(self):
        someotherval = False
        val = self.menu.add_value_button('Sir', someotherval)
        self.assertEqual(val.text, 'Sir', 'Given title not assigned to button')
        self.assertIn(val, self.menu._options, 'Button was returned but not added to its parent menu')

    def test_addValueButton_throwsIfUnsupportedType(self):
        someotherval = Group()
        with self.assertRaises(NotImplementedError):
            self.menu.add_value_button('Throw me', someotherval, 
                                    'ValueButton incorrectly believed it could handle type {}'.format(type(someotherval)))

    def test_addSubmenu_useDiscreteOptionsLists(self):
        alt_sub = Menu(DISPLAY, HEIGHT, WIDTH)
        self.menu.add_submenu_button('Alt menu', alt_sub)
        self.assertNotEqual(alt_sub._options, self.menu._options, 'Distinct child submenu references the same _options object as its parent')

    def test_addSubmenu_siblingsUseDiscreteOptionsLists(self):
        alt_sub = Menu(DISPLAY, HEIGHT, WIDTH)
        self.menu.add_submenu_button('Alt menu', alt_sub)
        alt_sub.add_submenu_button('Going deeper', Menu(DISPLAY, HEIGHT, WIDTH))

        dif_sub = Menu(DISPLAY, HEIGHT, WIDTH)
        self.menu.add_submenu_button('Dif menu', dif_sub)

        self.assertNotEqual(alt_sub._options, dif_sub._options, 'Distinct submenu siblings reference the same _options object')

    def test_addSubmenu_addsExitButton(self):
        btn_text = 'GO UP'
        submenu = Menu(DISPLAY, HEIGHT, WIDTH)
        og_len = len(submenu._options)
        
        self.menu.add_submenu_button('my btn', submenu, add_upmenu_btn=btn_text)
        new_len = len(submenu._options)
        self.assertNotEqual(og_len, new_len, 'NO Button was added to the submenu!')

        exit_btn = submenu._options[new_len - 1]
        self.assertEqual(btn_text, exit_btn.text, 'Added button text does not match expected')

    def test_showMenu_hasSubmenu(self):
        mock_submenu = Menu(get_mock_display(), HEIGHT, WIDTH)
        self.menu._activated_submenu = mock_submenu
        self.assertTrue(isinstance(self.menu.show_menu(), Group), 'Show_menu() did not return the displayio group it used')

    def test_showMenu_noSubmenu(self):
        self.assertTrue(isinstance(self.menu.show_menu(), Group), 'Show_menu() did not return the displayio group it used')

    def test_showMenu_hasAdjustMenu(self):
        mock_submenu = Mock(AdjustMenu('', HEIGHT, WIDTH), build_displayio_group=TRUE_ACTION)
        self.menu._activated_submenu = mock_submenu
        self.assertEqual(True, self.menu.show_menu(), 'Show_menu() did not return the displayio group it used')

    def test_click_clicksSubmenu(self):
        planted_return_value = True
        submenu = Menu(get_mock_display(), HEIGHT, WIDTH)
        submenu.click = Mock(return_value=planted_return_value)
        self.menu._activated_submenu = submenu
        is_open = self.menu.click()
        
        self.assertEqual(planted_return_value, is_open)
        submenu.click.assert_called_once()

    def test_click_hasAdjustMenu(self):
        adjust_submenu = AdjustMenu('label', HEIGHT, WIDTH)
        adjust_submenu.click = Mock(adjust_submenu.click)
        self.menu._activated_submenu = adjust_submenu
        is_open  = self.menu.click()

        self.assertTrue(is_open, 'The AdjustMenu did not return True as was expected')
        adjust_submenu.click.assert_called_once()

    def test_click_hasAdjustMenu_noInvokeSubClosing(self):
        planted_value = False
        adjust_submenu = AdjustMenu('label', HEIGHT, WIDTH)
        adjust_submenu.click = Mock(adjust_submenu.click, return_value=planted_value)
        self.menu._submenu_is_closing = Mock()
        self.menu._activated_submenu = adjust_submenu
        self.menu.click()
        
        self.menu._submenu_is_closing.assert_called_once()

    def test_click_clicksSelectedOption(self):
        selection = 1
        trap_mock = Mock(self.menu)
        trap_mock.click = Mock(side_effect=TRAP_ACTION)
        good_mock = Mock(self.menu)
        good_mock.click = Mock()

        self.menu._options = [trap_mock, good_mock, trap_mock, trap_mock]
        self.menu._selection = selection

        self.menu.click()
        trap_mock.click.assert_not_called()
        good_mock.click.assert_called_once()

    def test_scroll(self):
        return_value = 369
        submenu = Menu(get_mock_display(), HEIGHT, WIDTH)
        submenu.scroll = Mock(return_value=return_value)
        self.menu._activated_submenu = submenu

        position = self.menu.scroll(2)
        submenu.scroll.assert_called_once()
        self.assertEqual(return_value, position, 'The value that the menu returned is not the one the submenu gave it')

    def test_scroll_positiveDeltaIncrementsPosition(self):
        self.menu._selection = 0
        result = self.menu.scroll(44)
        self.assertEqual(result, self.menu._selection, 'Scroll did not return the same position it set in its menu')
        self.assertEqual(1, result, 'Post-scroll position should have been incremented by 1')

    def test_scroll_positiveDeltaOverscrollsToTop(self):
        self.menu._selection = 2
        self.menu._options = ['my length', 'is', 3]
        result = self.menu.scroll(31)
        self.assertEqual(result, self.menu._selection, 'Scroll did not return the same position it set in its menu')
        self.assertEqual(0, result, 'Menu did not scroll back to the first (0th) item')

    def test_scroll_negativeDeltaDecrementsPosition(self):
        self.menu._selection = 2
        self.menu._options = ['my length', 'is', 3]
        result = self.menu.scroll(-12)
        self.assertEqual(result, self.menu._selection, 'Scroll did not return the same position it set in its menu')
        self.assertEqual(1, result, 'Post-scroll position should have been decremented by 1')

    def test_scroll_negativeDeltaUnderscrollsToBottom(self):
        self.menu._selection = 0
        self.menu._options = ['my length', 'is', 3]
        result = self.menu.scroll(-1)
        self.assertEqual(result, self.menu._selection, 'Scroll did not return the same position it set in its menu')
        self.assertEqual(2, result, 'Menu did not scroll back to the last item')

    def test_scroll_zeroDeltaNoChange(self):
        self.menu._selection = 1
        self.menu._options = ['my length', 'is', 3]
        result = self.menu.scroll(0)
        self.assertEqual(result, self.menu._selection, 'Scroll did not return the same position it set in its menu')
        self.assertEqual(1, result, 'Menu scrolled with a delta of zero!')

    def test_submenuClosing_usesScrollOption(self):
        self.menu._selection = 1
        self.menu.show_menu = Mock()
        self.menu._submenu_is_closing()
        self.assertEqual(0, self.menu._selection, 'Menu should have scrolled to the top after closing submenu')
        self.menu.show_menu.assert_called_once()

    def test_submenuClosing_noScroll(self):
        self.menu._selection = 1
        self.menu.show_menu = Mock()
        self.menu._scroll_after_submenu = False
        self.menu._submenu_is_closing()
        self.assertEqual(1, self.menu._selection, 'Menu should not have scrolled after closing submenu')
        self.menu.show_menu.assert_called_once()

    def test_submenuOpening_notAdjustMenu(self):
        self.menu.show_menu = Mock()
        submenu = AbstractMenu()

        self.menu._submenu_is_opening(submenu)
        self.menu.show_menu.assert_not_called()
    
    def test_submenuOpening_adjustMenu(self):
        self.menu.show_menu = Mock()
        submenu = AdjustMenu('', HEIGHT, WIDTH)

        self.menu._submenu_is_opening(submenu)
        self.menu.show_menu.assert_called_once_with()

    def test_createMenu_matchesProperties(self):
        newMenu = self.menu.create_menu('New menu')
        self.assertEqual(self.menu._display, newMenu._display, 'The new menu was created with a different Display object')
        self.assertEqual(self.menu._height, newMenu._height, 'The new menu was created with a different height')
        self.assertEqual(self.menu._width, newMenu._width, 'The new menu was created with a different width')
        self.assertEqual(self.menu._show_title, newMenu._show_title, 'The new menu was created with a different ShowHeight setting')
        self.assertEqual('New menu', newMenu._title, 'The new menu was not created with the given title string')


class MenuBuildingTests(unittest.TestCase):
    def setUp(self):        
        pass

    def test_buildGroup_menuWithTitle(self):
        menu = Menu.without_display(HEIGHT * 4, WIDTH, show_menu_title=True)
        anothermenu = Menu(DISPLAY, HEIGHT, WIDTH)
        rando_valuo = True
        act = menu.add_action_button('New action', action=TRAP_ACTION)
        sub = menu.add_submenu_button('Expand...', anothermenu)
        val = menu.add_value_button('Volume', rando_valuo)
        grp = menu.build_displayio_group()
        self.assertIn(act, menu._options)
        self.assertIn(sub, menu._options)
        self.assertIn(val, menu._options)
        self.assertEqual(4, len(grp), 'Constructed group contains missing or unpected elements')


    def test_buildGroup_menuNoTitle(self):
        menu = Menu(DISPLAY, HEIGHT, WIDTH, show_menu_title=True)
        menu.add_action_button('Accio test results', action=TRAP_ACTION)
        grp = menu.build_displayio_group()
        self.assertEqual(2, len(grp), 'Constructed group contains unexpected elements')

    def test_buildGroup_highlightsExpected(self):
        chosen_selection = 1
        menu = Menu(DISPLAY, HEIGHT, WIDTH, show_menu_title=False)
        menu.add_action_button('I am not selected', TRAP_ACTION)
        menu.add_action_button('I AM selected', PRINT_ACTION)
        menu._selection = chosen_selection

        grp = menu.build_displayio_group()

        self.assertEqual(2, len(grp))
        self.assertEqual(OPT_TEXT_COLOR, grp[0].color)
        self.assertEqual(OPT_BACK_COLOR, grp[0].background_color)
        self.assertEqual(OPT_HIGHLIGHT_TEXT_COLOR, grp[chosen_selection].color)
        self.assertEqual(OPT_HIGHLIGHT_BACK_COLOR, grp[chosen_selection].background_color)