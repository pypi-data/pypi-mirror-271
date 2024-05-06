from box import Box


class Meta(Box):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
