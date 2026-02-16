def build_metadata(region, segment, source, page, draft=False):

    return {
        "region": region,
        "customer_segment": segment,
        "source_doc": source,
        "page_number": page,
        "draft": draft
    }
