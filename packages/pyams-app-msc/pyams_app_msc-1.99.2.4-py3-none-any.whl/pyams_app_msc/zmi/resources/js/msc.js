/* global MyAMS */

'use strict';


if (window.$ === undefined) {
    window.$ = MyAMS.$;
}


const msc = {

    /**
     * Catalog management
     */
    catalog: {

        changeActivity: (evt) => {
            const
                lang = $('html').attr('lang'),
                form = $(evt.currentTarget).parents('form'),
                reference = $('select[name$=".widgets.reference"]', form),
                reference_oid = reference.val(),
                title = $(`input[name$=".widgets.${lang}.title"]`, form),
                data_type = $('select[name$=".widgets.data_type"]', form);
            if (reference_oid) {
                MyAMS.require('ajax').then(() => {
                    MyAMS.ajax.get(`${window.location.origin}/api/content/rest/${reference_oid}/info`).then((result) => {
                        title.val(result.info.title);
                        if (result.info.data_type) {
                            data_type.val(result.info.data_type.name).trigger('change');
                        }
                    });
                });
            }
        },

        getPrincipalID: (evt) => {
            const
                source = $(evt.currentTarget),
                select = source.siblings('select'),
                principalId = select.val();
            MyAMS.require('modal').then(() => {
                MyAMS.modal.open(`edit-user-profile.html?principal_id=${principalId}`);
            })
        }
    },

    /**
     * Session management
     */
    session: {

        changeActivity: (evt) => {
            const
                lang = $('html').attr('lang'),
                form = $(evt.currentTarget).parents('form'),
                reference = $('select[name$=".widgets.activity"]', form),
                reference_oid = reference.val();
            if (reference_oid) {
                MyAMS.require('ajax').then(() => {
                    MyAMS.ajax.get(`${window.location.origin}/api/content/rest/${reference_oid}/info`).then((result) => {
                        const duration = result.info?.catalog_entry?.duration;
                        if (duration) {
                            const
                                start_date = $(`input[name$=".widgets.start_date"]`, form),
                                start_value = new Date(start_date.val()),
                                end_date = $(`input[id$="-widgets-end_date-dt"]`, form),
                                end_value = new Date(start_value.getTime() + (duration * 60000));
                            end_date.data('datetimepicker').date(end_value);
                        }
                    });
                });
            }
        }
    },

    /**
     * Calendar management
     */
    calendar: {

        /**
         * Boolean flag to check if calendars are synchronized
         */
        synchronized: localStorage.getItem('msc.synchronized') === 'true',
        transposed: localStorage.getItem('msc.transposed') === 'true',

        /**
         * Initialize calendar events handlers
         */
        init: (event, element, settings, veto) => {
            settings['eventContent'] = MyAMS.msc.calendar.setEventContent;
            settings['eventClassNames'] = MyAMS.msc.calendar.setEventClassNames;
            settings['eventDidMount'] = MyAMS.msc.calendar.renderedEvent;
            settings['dateClick'] = MyAMS.msc.calendar.addEvent;
            settings['eventClick'] = MyAMS.msc.calendar.showEvent;
            settings['eventDrop'] = MyAMS.msc.calendar.dropEvent;
            settings['eventResize'] = MyAMS.msc.calendar.resizeEvent;
            settings['eventReceive'] = MyAMS.msc.calendar.receiveEvent;
            settings['datesSet'] = MyAMS.msc.calendar.setDates;
        },

        /**
         * Refresh current view of calendar matching given room
         */
        refresh: (roomId, options) => {
            if (typeof(options) === 'object') {
                roomId = options.room_id;
            }
            const calendar = $(`.calendar[data-msc-room="${roomId}"]`).data('msc-calendar');
            if (calendar) {
                calendar.refetchEvents();
            }
        },

        /**
         * Refresh all calendars
         */
        refreshAll: () => {
            $('.calendar').each((idx, elt) => {
                $(elt).data('msc-calendar').refetchEvents();
            });
        },

        /**
         * Store new calendar instance as data attribute
         */
        afterInit: (event, element, calendar) => {
            element.data('msc-calendar', calendar);
            if (msc.calendar.transposed) {
                $('.calendar-wrapper').addClass('transposed')
                const button = $('a[href="MyAMS.msc.calendar.transpose"]');
                if (button.exists()) {
                    button.button('toggle')
                        .toggleClass('btn-light')
                        .toggleClass('btn-link')
                        .toggleClass('btn-secondary')
                        .toggleClass('border-secondary');
                }
            }
            if (msc.calendar.synchronized) {
                const button = $('a[href="MyAMS.msc.calendar.synchronize"]');
                if (button.exists()) {
                    button.button('toggle')
                        .toggleClass('btn-light')
                        .toggleClass('btn-link')
                        .toggleClass('btn-secondary')
                        .toggleClass('border-secondary');
                }
            }
        },

        setEventContent: (info) => {
            const title = info.event.title.split('\n');
            return {
                html: `<strong>${title[0]}</strong><br />${title[1] || ''}`
            }
        },

        setEventClassNames: (info) => {
            let styles = '';
            if (info.event.extendedProps.temporary) {
                styles = 'font-italic';
            }
            if (info.event.extendedProps.borderWidth) {
                styles += ` border-${info.event.extendedProps.borderWidth}`;
            }
            if (info.event.extendedProps.borderStyle) {
                styles += ` border-${info.event.extendedProps.borderStyle}`;
            }
            return styles;
        },

        renderedEvent: (info) => {
            const elt = $(info.el);
            elt.data('msc-event', info.event)
                .contextMenu({
                    menuSelector: '#eventMenu'
                });
            const title = info.event.title.split('\n');
            elt.tooltip({
                title: `<strong>${title[0]}</strong><br />Places: ${title[1].replace(/\(/, '').replace(/\)/, '') || ''}`,
                html: true
            });
        },

        /**
         * Transpose plannings
         */
        transpose: (source) => {
            const wrapper = $('.calendar-wrapper');
            wrapper.toggleClass('transposed');
            $('.calendar').each((idx, elt) => {
                $(elt).data('msc-calendar').render();
            });
            source.button('toggle')
                .toggleClass('btn-light')
                .toggleClass('btn-link')
                .toggleClass('btn-secondary')
                .toggleClass('border-secondary');
            const transposed = wrapper.hasClass('transposed');
            localStorage.setItem('msc.transposed', transposed);
            msc.calendar.transposed = transposed;
        },

        /**
         * Synchronize calendars views and navigation
         */
        synchronize: (source) => {
            msc.calendar.synchronized = !msc.calendar.synchronized;
            if (msc.calendar.synchronized) {
                const
                    calendars = $('.calendar'),
                    firstPlugin = calendars.first().data('msc-calendar');
                try {
                    msc.calendar.synchronized = false;
                    calendars.each((idx, elt) => {
                        if (idx === 0) {
                            return;
                        }
                        const plugin = $(elt).data('msc-calendar');
                        plugin.changeView(firstPlugin.view.type, firstPlugin.view.currentStart);
                    });
                } finally {
                    msc.calendar.synchronized = true;
                }
            }
            source.button('toggle')
                .toggleClass('btn-light')
                .toggleClass('btn-link')
                .toggleClass('btn-secondary')
                .toggleClass('border-secondary');
            localStorage.setItem('msc.synchronized', source.hasClass('btn-secondary'));
        },

        /**
         * List of calendar being updated
         */
        updating: [],

        /**
         * Synchronize calendars dates changes
         */
        setDates: (dateInfo) => {

            function clearUpdates() {
                msc.calendar.updating.splice(0, msc.calendar.updating.length);
            }

            $('.tooltip').tooltip('hide');
            if (!msc.calendar.synchronized) {
                return;
            }
            const updating = msc.calendar.updating;
            if (updating.indexOf(dateInfo.view.calendar) > -1) {
                return;
            }
            updating.push(dateInfo.view.calendar);
            const calendars = $('.calendar');
            try {
                calendars.each((idx, elt) => {
                    const calendar = $(elt),
                          plugin = calendar.data('msc-calendar');
                    if (plugin) {
                        if ((updating.indexOf(plugin) > -1) || (plugin === dateInfo.view.calendar)) {
                            return;
                        }
                        plugin.changeView(dateInfo.view.type, dateInfo.view.currentStart);
                    }
                });
            } finally {
                setTimeout(clearUpdates, 50);
            }
        },

        /**
         * Add new event to calendar
         */
        addEvent: (info) => {
            const source = info.jsEvent.target,
                  calendar = $(source).parents('.calendar'),
                  room = calendar.data('msc-room');
            $('.tooltip').tooltip('hide');
            if (calendar.data('msc-editable') !== 'True') {
                return;
            }
            MyAMS.require('modal').then(() => {
                MyAMS.modal.open('add-session.html', {
                    start: info.dateStr,
                    room: room
                });
            });
        },

        cloneEvent: (menu, source) => {
            return () => {
                $('.tooltip').tooltip('hide');
                MyAMS.require('ajax').then(() => {
                    const event = source.data('msc-event');
                    MyAMS.ajax.post(`${event.extendedProps.href}/clone-event.json`).then((result) => {
                        if (result.status === 'success') {
                            MyAMS.msc.calendar.refresh(result.event.room);
                        }
                    });
                });
            };
        },

        /**
         * Update calendar after event creation
         */
        addEventCallback: (form, options) => {
            const
                event = options.event,
                roomName = event.room;
            $('.tooltip').tooltip('hide');
            MyAMS.msc.calendar.refresh(roomName);
        },

        /**
         * Show event properties on click
         */
        showEvent: (info) => {
            const
                event = info.event,
                visible = event.extendedProps?.visible;
            $('.tooltip').tooltip('hide');
            if (visible) {
                const href = event.extendedProps?.href;
                if (href) {
                    MyAMS.require('modal').then(() => {
                        MyAMS.modal.open(`${href}/properties.html`);
                    });
                }
            }
        },

        /**
         * Update calendars after event update
         */
        editEventCallback: (form, options) => {
            const
                event = options.event,
                eventRoomName = event.room.toString(),
                calendars = $('.calendar');
            $('.tooltip').tooltip('hide');
            calendars.each((idx, elt) => {
                const
                    calendar = $(elt),
                    calendarRoomName = calendar.data('msc-room').toString(),
                    plugin = calendar.data('msc-calendar');
                if (calendarRoomName === eventRoomName) {
                    plugin.refetchEvents();
                } else {  // old event room
                    const oldEvent = plugin.getEventById(event.id);
                    if (oldEvent) {
                        oldEvent.remove();
                    }
                }
            });
        },

        /**
         * Change event by drag & drop on same calendar
         */
        dropEvent: (info) => {
            $('.tooltip').tooltip('hide');
            return new Promise((resolve, reject) => {
                const
                    event = info.event,
                    href = event.extendedProps?.href;
                if (href) {
                    MyAMS.require('ajax').then(() => {
                        MyAMS.ajax.post(`${href}/update-event.json`, {
                            room: event.extendedProps.room.toString(),
                            start: event.startStr,
                            end: event.endStr
                        }).then(result => {
                            resolve(result);
                        }, () => {
                            info.revert();
                            reject();
                        });
                    });
                } else {
                    info.revert();
                    reject();
                }
            });
        },

        /**
         * Update event duration by drag & drop
         */
        resizeEvent: (info) => {
            $('.tooltip').tooltip('hide');
            return new Promise((resolve, reject) => {
                const
                    event = info.event,
                    href = event.extendedProps?.href;
                if (href) {
                    MyAMS.require('ajax').then(() => {
                        MyAMS.ajax.post(`${href}/update-event.json`, {
                            room: event.extendedProps.room.toString(),
                            start: event.startStr,
                            end: event.endStr
                        }).then(result => {
                            resolve(result);
                        }, () => {
                            info.revert();
                            reject();
                        });
                    });
                } else {
                    info.revert();
                    reject();
                }
            });
        },

        /**
         * Drag event to another calendar
         */
        receiveEvent: (info) => {
            $('.tooltip').tooltip('hide');
            return new Promise((resolve, reject) => {
                const
                    event = info.event,
                    href = event.extendedProps?.href;
                if (href) {
                    const target = $(info.view.calendar.el),
                          targetPlugin = target.data('msc-calendar'),
                          targetRoom = target.data('msc-room'),
                          sourceRoom = event.extendedProps?.room,
                          sourcePlugin = $(`.calendar[data-msc-room="${sourceRoom}"]`).data('msc-calendar');
                    MyAMS.require('ajax').then(() => {
                        MyAMS.ajax.post(`${href}/update-event.json`, {
                            room: targetRoom.toString(),
                            start: event.startStr,
                            end: event.endStr
                        }).then(result => {
                            info.revert();
                            sourcePlugin.refetchEvents();
                            targetPlugin.refetchEvents();
                            if (result.messagebox) {
                                MyAMS.require('alert').then(() => {
                                    MyAMS.alert.messageBox(result.messagebox);
                                    resolve(result);
                                });
                            } else {
                                resolve(result);
                            }
                        }, () => {
                            info.revert();
                            sourcePlugin.refetchEvents();
                            targetPlugin.refetchEvents();
                            reject();
                        });
                    });
                } else {
                    info.revert();
                    reject();
                }
            });
        },

        /**
         * Delete event callback
         */
        deleteEventCallback: (form, options) => {
            const calendar = $(`.calendar[data-msc-room="${options.room}"]`),
                  plugin = calendar.data('msc-calendar'),
                  event = plugin.getEventById(options.event_id);
            $('.tooltip').tooltip('hide');
            if (event) {
                event.remove();
            }
        },

        /**
         * Manage event booking
         */
        manageEventBookings: (menu, source) => {
            return () => {
                const event = source.data('msc-event');
                MyAMS.require('modal').then(() => {
                    MyAMS.modal.open(`${event.extendedProps.href}/bookings.html`);
                });
            }
        }
    },

    /**
     * Bookings management
     */
    booking: {

        /**
         * Booking price changed
         */
        priceChanged: (source) => {
            MyAMS.require('ajax').then(() => {
                const
                    select2 = source.select2,
                    value = select2.val(),
                    form = $(select2.$element).parents('form'),
                    ratio = $(`input[name="form.widgets.accompanying_ratio"]`, form),
                    params = {};
                if (value && (value !== '--NOVALUE--')) {
                    params[source.amsSelect2HelperArgument] = value;
                    MyAMS.ajax.get(source.amsSelect2HelperUrl, params).then(result => {
                        ratio.val(result.price.accompanying_ratio);
                    });
                } else {
                    ratio.val(null);
                }
            });
        },

        /**
         * Booking session change
         */
        changeSession: (form, options) => {
            const
                oldSession = options.old_session,
                newSession = options.new_session;
            if (oldSession !== newSession) {
                const
                    rowId = options.row_id,
                    row = $(`tr[id="${rowId}"]`),
                    table = row.parents('table');
                if (table.hasClass('datatable')) {
                    table.DataTable().row(row).remove().draw();
                } else {
                    row.remove();
                }
            }
            MyAMS.msc.calendar.refreshAll();
        },

        /**
         * Quotation preview
         */
        previewQuotation: (evt, options) => {
            MyAMS.require('ajax', 'alert').then(() => {
                const
                    form = $(evt.currentTarget).parents('form'),
                    nb_participants = $(`input[name="form.widgets.nb_participants"]`, form).val(),
                    nb_accompanists = $(`input[name="form.widgets.nb_accompanists"]`, form).val(),
                    price = $(`select[name="form.widgets.price"]`, form).val(),
                    ratio = $(`input[name="form.widgets.accompanying_ratio"]`, form).val();
                if (!nb_participants ||
                    !nb_accompanists ||
                    (!price || (price === '--NOVALUE--'))) {
                    MyAMS.alert.messageBox({
                        status: 'error',
                        title: "Prévisualisation impossible !",
                        message: "Vous devez définir le nombre de participants et " +
                            "sélectionner un tarif pour pouvoir prévisualiser le devis..."
                    });
                } else {
                    window.open(`${options.target}?` +
                        `nb_participants=${nb_participants}&` +
                        `nb_accompanists=${nb_accompanists}&` +
                        `price=${price}&` +
                        `ratio=${ratio || 0}`, '_blank');
                }
            });
        },

        /**
         * Quotation reset
         */
        resetQuotation: (evt, options) => {
            const target = options.target;
            MyAMS.require('ajax').then(() => {
                MyAMS.ajax.post(target, {}).then(MyAMS.ajax.handleJSON);
            });
        }
    }
};


if (window.MyAMS) {
    MyAMS.config.modules.push('msc');
    MyAMS.msc = msc;
    console.debug("MyAMS: MSC module loaded...");
}
