-- Section-break slides (a level-1 heading) and the title slide sit on the
-- brand primary; content slides stay on paper. The colour is named through
-- the custom property the brand layer emits, so no colour lives here, and
-- reveal still gets a value it can act on: it resolves the variable, then
-- adds `has-dark-background` to the slide so headings, text and chrome flip
-- to the light palette on their own.
--
-- A deck can override either: `{background-color="..."}` on the heading, or
-- `title-slide-attributes:` in the front matter.

local SECTION_BACKGROUND = "var(--brand-indigo)"

return {
  {
    Meta = function(meta)
      local attrs = meta["title-slide-attributes"] or pandoc.MetaMap({})
      if attrs["data-background-color"] == nil then
        attrs["data-background-color"] = pandoc.MetaString(SECTION_BACKGROUND)
      end
      -- The running footer repeats the subtitle, which the title slide
      -- already shows in full.
      if attrs["data-footer"] == nil then
        attrs["data-footer"] = pandoc.MetaString("false")
      end
      meta["title-slide-attributes"] = attrs
      return meta
    end,

    Header = function(el)
      if el.level == 1 then
        if el.attributes["background-color"] == nil then
          el.attributes["background-color"] = SECTION_BACKGROUND
        end
        -- One line on a coloured field; the running footer would only clutter it.
        if el.attributes["data-footer"] == nil then
          el.attributes["data-footer"] = "false"
        end
      end
      return el
    end,
  },
}
