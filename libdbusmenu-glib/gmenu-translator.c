#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "gmenu-translator.h"

struct _DbusmenuGmenuTranslatorPrivate {
	int dummy;
};

#define DBUSMENU_GMENU_TRANSLATOR_GET_PRIVATE(o) \
(G_TYPE_INSTANCE_GET_PRIVATE ((o), DBUSMENU_TYPE_GMENU_TRANSLATOR, DbusmenuGmenuTranslatorPrivate))

static void dbusmenu_gmenu_translator_class_init (DbusmenuGmenuTranslatorClass *klass);
static void dbusmenu_gmenu_translator_init       (DbusmenuGmenuTranslator *self);
static void dbusmenu_gmenu_translator_dispose    (GObject *object);
static void dbusmenu_gmenu_translator_finalize   (GObject *object);

G_DEFINE_TYPE (DbusmenuGmenuTranslator, dbusmenu_gmenu_translator, G_TYPE_OBJECT);

static void
dbusmenu_gmenu_translator_class_init (DbusmenuGmenuTranslatorClass *klass)
{
	GObjectClass *object_class = G_OBJECT_CLASS (klass);

	g_type_class_add_private (klass, sizeof (DbusmenuGmenuTranslatorPrivate));

	object_class->dispose = dbusmenu_gmenu_translator_dispose;
	object_class->finalize = dbusmenu_gmenu_translator_finalize;
}

static void
dbusmenu_gmenu_translator_init (DbusmenuGmenuTranslator *self)
{
}

static void
dbusmenu_gmenu_translator_dispose (GObject *object)
{

	G_OBJECT_CLASS (dbusmenu_gmenu_translator_parent_class)->dispose (object);
}

static void
dbusmenu_gmenu_translator_finalize (GObject *object)
{

	G_OBJECT_CLASS (dbusmenu_gmenu_translator_parent_class)->finalize (object);
}
