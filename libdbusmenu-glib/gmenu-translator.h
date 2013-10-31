#ifndef __DBUSMENU_GMENU_TRANSLATOR_H__
#define __DBUSMENU_GMENU_TRANSLATOR_H__

#include <glib.h>
#include <glib-object.h>

G_BEGIN_DECLS

#define DBUSMENU_TYPE_GMENU_TRANSLATOR            (dbusmenu_gmenu_translator_get_type ())
#define DBUSMENU_GMENU_TRANSLATOR(obj)            (G_TYPE_CHECK_INSTANCE_CAST ((obj), DBUSMENU_TYPE_GMENU_TRANSLATOR, DbusmenuGmenuTranslator))
#define DBUSMENU_GMENU_TRANSLATOR_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST ((klass), DBUSMENU_TYPE_GMENU_TRANSLATOR, DbusmenuGmenuTranslatorClass))
#define DBUSMENU_IS_GMENU_TRANSLATOR(obj)         (G_TYPE_CHECK_INSTANCE_TYPE ((obj), DBUSMENU_TYPE_GMENU_TRANSLATOR))
#define DBUSMENU_IS_GMENU_TRANSLATOR_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE ((klass), DBUSMENU_TYPE_GMENU_TRANSLATOR))
#define DBUSMENU_GMENU_TRANSLATOR_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS ((obj), DBUSMENU_TYPE_GMENU_TRANSLATOR, DbusmenuGmenuTranslatorClass))

typedef struct _DbusmenuGmenuTranslator          DbusmenuGmenuTranslator;
typedef struct _DbusmenuGmenuTranslatorClass     DbusmenuGmenuTranslatorClass;
typedef struct _DbusmenuGmenuTranslatorPrivate   DbusmenuGmenuTranslatorPrivate;

struct _DbusmenuGmenuTranslatorClass {
	GObjectClass parent_class;
};

struct _DbusmenuGmenuTranslator {
	GObject parent;
};

GType dbusmenu_gmenu_translator_get_type (void);

G_END_DECLS

#endif
