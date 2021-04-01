#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod clone;

use gtk::prelude::*;
use gio::prelude::*;

use gtk::Window;
use std::path::PathBuf;

fn show_text(parent_window: &impl IsA<Window>, text: String) {
    let dialog = gtk::MessageDialogBuilder::new()
        .text(&text)
        .buttons(gtk::ButtonsType::Ok)
        .modal(true)
        .transient_for(parent_window)
        .build();
    dialog.show_all();
    dialog.connect_response(|dialog, _| dialog.close());
}

fn open_file_chooser(mime_filter: &str) -> Option<PathBuf> {
    let file_filter = gtk::FileFilter::new();
    file_filter.add_mime_type(mime_filter);
    let file_chooser = gtk::FileChooserNativeBuilder::new()
        .filter(&file_filter)
        .build();

    if file_chooser.run() == gtk::ResponseType::Accept {
        let path = file_chooser.get_filename().unwrap();
        Some(path)
    } else {
        None
    }
}

fn recognize_text_in_separate_thread_and_show_results(path: PathBuf, window: &impl IsA<Window>) {
    let (sender, receiver) = glib::MainContext::channel(glib::PRIORITY_DEFAULT);

    std::thread::spawn(move || {
        let mut lt = leptess::LepTess::new(Some("./tessdata"), "eng+rus").unwrap();
        lt.set_image(path).unwrap();
        let text: String = lt.get_utf8_text().unwrap();
        sender.send(text).unwrap();
    });

    receiver.attach(None, {clone!(window); move |text| {
        show_text(&window, text);
        glib::Continue(false)
    }});
}

fn main() {
    let application = gtk::Application::new(None, Default::default()).unwrap();

    application.connect_activate(|application| {
        let window = gtk::ApplicationWindowBuilder::new()
            .application(application)
            .title("Text from image")
            .default_width(600)
            .default_height(400)
            .build();

        let button = gtk::Button::with_label("Open");
        button.connect_clicked({clone!(window); move |_| {
            if let Some(path) = open_file_chooser("image/*") {
                recognize_text_in_separate_thread_and_show_results(path, &window);
            }
        }});
        window.add(&button);

        window.show_all();
    });

    application.run(&[]);
}
