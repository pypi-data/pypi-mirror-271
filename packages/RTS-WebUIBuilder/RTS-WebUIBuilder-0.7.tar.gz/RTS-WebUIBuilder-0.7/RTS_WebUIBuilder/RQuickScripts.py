
class RQuickScripts:
    def __init__(self): 
        self.qscript = ""
        pass

    def redirectFunction(self):
        string = '''
<script>
   function redirect(tourl) {
      window.location.href = tourl;
   }
</script>'''
        self.qscript = string  
    def get(self):
        return self.qscript